from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Patient routes
patients = Blueprint("patients", __name__)


# Get all patients accessible to the user
# Available to Doctor-1.1 and Nurse-2.1
@patients.route("/patients", methods=["GET"])
def get_all_patients():
    try:
        current_app.logger.info('Starting get_all_patients request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Patient")
        patients_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(patients_data)} patients')
        return jsonify(patients_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_patients: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get details for a specific patient
# Available to Doctor-1.1, Nurse-2.5, and Patient-3.4
@patients.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            return jsonify({"error": "Patient not found"}), 404
            
        cursor.close()
        return jsonify(patient), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update patient information (link DischargeID or ConditionID)
# Available to Doctor-1.4
@patients.route("/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["DischargeID", "ConditionID", "DoctorID", "NurseID", "VitalID", "VisitID"]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])
        
        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(patient_id)
        query = f"UPDATE Patient SET {', '.join(update_fields)} WHERE PatientID = %s"
        
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Patient updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get medications associated with a patient (via Patient_Medications join)
# Available to Patient-3.5 and Proxy-4.4
@patients.route("/patients/<int:patient_id>/medications", methods=["GET"])
def get_patient_medications(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient medications with medication details
        query = """
        SELECT pm.*, m.PrescriptionName, m.DosageAmount, m.DosageUnit, 
               m.PickUpLocation, m.RefillsLeft, m.FrequencyAmount, m.FrequencyPeriod
        FROM Patient_Medications pm
        JOIN Medication m ON pm.MedicationID = m.MedicationID
        WHERE pm.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        medications = cursor.fetchall()
        cursor.close()
        
        return jsonify(medications), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get proxy information if one exists for the patient
# Available to Proxy-4.1
@patients.route("/patients/<int:patient_id>/proxy", methods=["GET"])
def get_patient_proxy(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get proxy information
        cursor.execute("SELECT * FROM Proxy WHERE PatientID = %s", (patient_id,))
        proxies = cursor.fetchall()
        cursor.close()
        
        return jsonify(proxies), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's current visit (using Patient.VisitID as FK)
# Available to Patient-3.6 and Proxy-4.2
@patients.route("/patients/<int:patient_id>/visit", methods=["GET"])
def get_patient_visit(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's current visit
        query = """
        SELECT v.* FROM Visits v
        JOIN Patient p ON v.VisitID = p.VisitID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        visit = cursor.fetchone()
        cursor.close()
        
        if not visit:
            return jsonify({"message": "No visit found for this patient"}), 404
            
        return jsonify(visit), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's current vitals (via Patient.VitalID FK)
# Available to Doctor-1.2 and Nurse-2.1
@patients.route("/patients/<int:patient_id>/vitals", methods=["GET"])
def get_patient_vitals(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's current vitals
        query = """
        SELECT v.* FROM VitalChart v
        JOIN Patient p ON v.VitalID = p.VitalID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        vitals = cursor.fetchone()
        cursor.close()
        
        if not vitals:
            return jsonify({"message": "No vitals found for this patient"}), 404
            
        return jsonify(vitals), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's condition (via Patient.ConditionID FK)
# Available to Doctor-1.1 and Proxy-4.3
@patients.route("/patients/<int:patient_id>/condition", methods=["GET"])
def get_patient_condition(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's condition
        query = """
        SELECT c.* FROM `Condition` c
        JOIN Patient p ON c.ConditionID = p.ConditionID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        condition = cursor.fetchone()
        cursor.close()
        
        if not condition:
            return jsonify({"message": "No condition found for this patient"}), 404
            
        return jsonify(condition), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's discharge (via Patient.DischargeID FK)
# Available to Patient-3.2 and Proxy-4.5
@patients.route("/patients/<int:patient_id>/discharge", methods=["GET"])
def get_patient_discharge(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's discharge information
        query = """
        SELECT d.* FROM Discharge d
        JOIN Patient p ON d.DischargeID = p.DischargeID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        discharge = cursor.fetchone()
        cursor.close()
        
        if not discharge:
            return jsonify({"message": "No discharge found for this patient"}), 404
            
        return jsonify(discharge), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's doctor (via Patient.DoctorID FK)
# Available to Patient-3.4 and Proxy-4.6
@patients.route("/patients/<int:patient_id>/doctor", methods=["GET"])
def get_patient_doctor(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's doctor
        query = """
        SELECT d.* FROM Doctor d
        JOIN Patient p ON d.DoctorID = p.DoctorID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        doctor = cursor.fetchone()
        cursor.close()
        
        if not doctor:
            return jsonify({"message": "No doctor assigned to this patient"}), 404
            
        return jsonify(doctor), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's nurse (via Patient.NurseID FK)
# Available to Proxy-4.6
@patients.route("/patients/<int:patient_id>/nurse", methods=["GET"])
def get_patient_nurse(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's nurse
        query = """
        SELECT n.* FROM Nurse n
        JOIN Patient p ON n.NurseID = p.NurseID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        nurse = cursor.fetchone()
        cursor.close()
        
        if not nurse:
            return jsonify({"message": "No nurse assigned to this patient"}), 404
            
        return jsonify(nurse), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get patient's insurance (via Patient.InsuranceID FK)
@patients.route("/patients/<int:patient_id>/insurance", methods=["GET"])
def get_patient_insurance(patient_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if patient exists
        cursor.execute("SELECT * FROM Patient WHERE PatientID = %s", (patient_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Patient not found"}), 404
        
        # Get patient's insurance
        query = """
        SELECT i.* FROM Insurance i
        JOIN Patient p ON i.InsuranceID = p.InsuranceID
        WHERE p.PatientID = %s
        """
        cursor.execute(query, (patient_id,))
        insurance = cursor.fetchone()
        cursor.close()
        
        if not insurance:
            return jsonify({"message": "No insurance found for this patient"}), 404
            
        return jsonify(insurance), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
