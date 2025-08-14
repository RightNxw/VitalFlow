from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Condition routes
conditions = Blueprint("conditions", __name__)


# Get all conditions
@conditions.route("/", methods=["GET"])
def get_all_conditions():
    try:
        current_app.logger.info('Starting get_all_conditions request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM `Condition`")
        conditions_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(conditions_data)} conditions')
        return jsonify(conditions_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_conditions: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new condition
# Available to Doctor-1.1
@conditions.route("/", methods=["POST"])
def create_condition():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["Description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new condition
        query = """
        INSERT INTO `Condition` (Description, Treatment)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (
                data["Description"],
                data.get("Treatment")  # Optional field
            ),
        )
        
        db.get_db().commit()
        new_condition_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Condition created successfully", "condition_id": new_condition_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get details for a specific condition
# Available to Doctor-1.1 and Proxy-4.3
@conditions.route("/<int:condition_id>", methods=["GET"])
def get_condition(condition_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM `Condition` WHERE ConditionID = %s", (condition_id,))
        condition = cursor.fetchone()
        
        if not condition:
            return jsonify({"error": "Condition not found"}), 404
            
        cursor.close()
        return jsonify(condition), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update condition information
# Available to Nurse-2.2
@conditions.route("/<int:condition_id>", methods=["PUT"])
def update_condition(condition_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Check if condition exists
        cursor.execute("SELECT * FROM `Condition` WHERE ConditionID = %s", (condition_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Condition not found"}), 404
        
        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["Description", "Treatment"]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(condition_id)
        query = f"UPDATE `Condition` SET {', '.join(update_fields)} WHERE ConditionID = %s"
        
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Condition updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
