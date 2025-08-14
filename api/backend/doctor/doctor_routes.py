from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Doctor routes
doctors = Blueprint("doctors", __name__)


# Get all doctors
# Available to Patient-3.4
@doctors.route("/", methods=["GET"])
def get_all_doctors():
    try:
        current_app.logger.info('Starting get_all_doctors request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Doctor")
        doctors_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(doctors_data)} doctors')
        return jsonify(doctors_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_doctors: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get a specific doctor
@doctors.route("/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Doctor WHERE DoctorID = %s", (doctor_id,))
        doctor = cursor.fetchone()
        
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404
            
        cursor.close()
        return jsonify(doctor), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
