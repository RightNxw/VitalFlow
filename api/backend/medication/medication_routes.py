from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Medication routes
medications = Blueprint("medications", __name__)


# Get all medications
@medications.route("/medications", methods=["GET"])
def get_all_medications():
    try:
        current_app.logger.info('Starting get_all_medications request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Medication")
        medications_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(medications_data)} medications')
        return jsonify(medications_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_medications: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create a new medication
# Available to Doctor-1.3
@medications.route("/medications", methods=["POST"])
def create_medication():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["PrescriptionName"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new medication
        query = """
        INSERT INTO Medication (PrescriptionName, DosageAmount, DosageUnit, PickUpLocation, 
                              RefillsLeft, FrequencyAmount, FrequencyPeriod)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["PrescriptionName"],
                data.get("DosageAmount"),
                data.get("DosageUnit"),
                data.get("PickUpLocation"),
                data.get("RefillsLeft"),
                data.get("FrequencyAmount"),
                data.get("FrequencyPeriod")
            ),
        )
        
        db.get_db().commit()
        new_medication_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Medication created successfully", "medication_id": new_medication_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get a specific medication with all details
# Available to Patient-3.5 and Proxy-4.4
@medications.route("/medications/<int:medication_id>", methods=["GET"])
def get_medication(medication_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Medication WHERE MedicationID = %s", (medication_id,))
        medication = cursor.fetchone()
        
        if not medication:
            return jsonify({"error": "Medication not found"}), 404
            
        cursor.close()
        return jsonify(medication), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all patient-medication links
@medications.route("/patient-medication", methods=["GET"])
def get_all_patient_medications():
    try:
        current_app.logger.info('Starting get_all_patient_medications request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Patient_Medications")
        patient_medications = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(patient_medications)} patient-medication links')
        return jsonify(patient_medications), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_patient_medications: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Link patient to medication
# Available to Doctor-1.3
@medications.route("/patient-medication", methods=["POST"])
def link_patient_medication():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["PatientID", "MedicationID"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (data["PatientID"],))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Check if medication exists
        cursor.execute("SELECT * FROM Medication WHERE MedicationID = %s", (data["MedicationID"],))
        if not cursor.fetchone():
            return jsonify({"error": "Medication not found"}), 404
        
        # Insert patient-medication link
        query = """
        INSERT INTO Patient_Medications (PatientID, MedicationID, PrescribedDate, EndDate)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["PatientID"],
                data["MedicationID"],
                data.get("PrescribedDate"),
                data.get("EndDate")
            ),
        )
        
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Patient linked to medication successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
