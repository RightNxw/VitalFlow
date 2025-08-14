from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Vital Chart routes
vitals = Blueprint("vitals", __name__)


# Get all vital charts
@vitals.route("/", methods=["GET"])
def get_all_vital_charts():
    try:
        current_app.logger.info('Starting get_all_vitalcharts request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM VitalChart")
        vitals_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(vitals_data)} vital charts')
        return jsonify(vitals_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_vitalcharts: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new vital chart
# Available to Nurse-2.1
@vitals.route("/", methods=["POST"])
def create_vital_chart():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["HeartRate", "BloodPressure", "RespiratoryRate", "Temperature"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new vital chart
        query = """
        INSERT INTO VitalChart (HeartRate, BloodPressure, RespiratoryRate, Temperature)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["HeartRate"],
                data["BloodPressure"],
                data["RespiratoryRate"],
                data["Temperature"]
            ),
        )
        
        db.get_db().commit()
        new_vital_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Vital chart created successfully", "vital_id": new_vital_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get details for a specific vital chart
@vitals.route("/<int:vital_id>", methods=["GET"])
def get_vital_chart(vital_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM VitalChart WHERE VitalID = %s", (vital_id,))
        vital = cursor.fetchone()
        
        if not vital:
            return jsonify({"error": "Vital chart not found"}), 404
            
        cursor.close()
        return jsonify(vital), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
