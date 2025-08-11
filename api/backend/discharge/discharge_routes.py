from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Discharge routes
discharges = Blueprint("discharges", __name__)


# Get all discharge records
@discharges.route("/discharge", methods=["GET"])
def get_all_discharges():
    try:
        current_app.logger.info('Starting get_all_discharges request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Discharge")
        discharges_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(discharges_data)} discharges')
        return jsonify(discharges_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_discharges: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create discharge with DischargeDate and Instructions
# Available to Doctor-1.4
@discharges.route("/discharge", methods=["POST"])
def create_discharge():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["DischargeDate", "Instructions"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new discharge
        query = """
        INSERT INTO Discharge (DischargeDate, Instructions)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (
                data["DischargeDate"],
                data["Instructions"]
            ),
        )
        
        db.get_db().commit()
        new_discharge_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Discharge created successfully", "discharge_id": new_discharge_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get discharge details
# Available to Patient-3.2 and Proxy-4.5
@discharges.route("/discharge/<int:discharge_id>", methods=["GET"])
def get_discharge(discharge_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Discharge WHERE DischargeID = %s", (discharge_id,))
        discharge = cursor.fetchone()
        
        if not discharge:
            return jsonify({"error": "Discharge not found"}), 404
            
        cursor.close()
        return jsonify(discharge), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
