from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Visit routes
visits = Blueprint("visits", __name__)


# Get all visits
@visits.route("/visits", methods=["GET"])
def get_all_visits():
    try:
        current_app.logger.info('Starting get_all_visits request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Visits")
        visits_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(visits_data)} visits')
        return jsonify(visits_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_visits: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new visit
@visits.route("/visits", methods=["POST"])
def create_visit():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["AdmitReason", "AppointmentDate"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new visit
        query = """
        INSERT INTO Visits (AdmitReason, AppointmentDate, NextVisitDate)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["AdmitReason"],
                data["AppointmentDate"],
                data.get("NextVisitDate")  # Optional field
            ),
        )
        
        db.get_db().commit()
        new_visit_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Visit created successfully", "visit_id": new_visit_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get details for a specific visit
# Available to Proxy-4.2, Patient-3.6, and Proxy-4.5
@visits.route("/visits/<int:visit_id>", methods=["GET"])
def get_visit(visit_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Visits WHERE VisitID = %s", (visit_id,))
        visit = cursor.fetchone()
        
        if not visit:
            return jsonify({"error": "Visit not found"}), 404
            
        cursor.close()
        return jsonify(visit), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update visit information (such as NextVisitDate)
@visits.route("/visits/<int:visit_id>", methods=["PUT"])
def update_visit(visit_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Check if visit exists
        cursor.execute("SELECT * FROM Visits WHERE VisitID = %s", (visit_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Visit not found"}), 404
        
        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["AdmitReason", "AppointmentDate", "NextVisitDate"]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(visit_id)
        query = f"UPDATE Visits SET {', '.join(update_fields)} WHERE VisitID = %s"
        
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Visit updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
