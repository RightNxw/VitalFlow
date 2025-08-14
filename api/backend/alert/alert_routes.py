from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app
from datetime import datetime

# Create a Blueprint for Alert routes
alerts = Blueprint("alerts", __name__)


# Get alerts for a user (accessible via AlertsDoctors or AlertsNurse)
# Available to Nurse-2.3 and Proxy-4.1
@alerts.route("/", methods=["GET"])
def get_alerts():
    try:
        current_app.logger.info('Starting get_alerts request')
        cursor = db.get_db().cursor()
        
        # Get query parameters for filtering by user type and ID
        user_type = request.args.get("user_type")  # "doctor" or "nurse"
        user_id = request.args.get("user_id")
        
        if not user_type or not user_id:
            return jsonify({"error": "user_type and user_id parameters are required"}), 400
        
        # Get alerts based on user type
        if user_type == "doctor":
            query = """
            SELECT ad.* FROM AlertDetails ad
            JOIN AlertsDoctors ald ON ad.AlertID = ald.AlertID
            WHERE ald.DoctorID = %s
            ORDER BY ad.SentTime DESC
            """
        elif user_type == "nurse":
            query = """
            SELECT ad.* FROM AlertDetails ad
            JOIN AlertsNurse aln ON ad.AlertID = aln.AlertID
            WHERE aln.NurseID = %s
            ORDER BY ad.SentTime DESC
            """
        else:
            return jsonify({"error": "Invalid user_type. Must be 'doctor' or 'nurse'"}), 400
        
        cursor.execute(query, (user_id,))
        alerts_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(alerts_data)} alerts for {user_type} {user_id}')
        return jsonify(alerts_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_alerts: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create alert with UrgencyLevel and Protocol
@alerts.route("/", methods=["POST"])
def create_alert():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["Message", "SentTime", "PostedBy", "PostedByRole", "UrgencyLevel", "Protocol"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate UrgencyLevel (1-5)
        urgency_level = int(data["UrgencyLevel"])
        if not (1 <= urgency_level <= 5):
            return jsonify({"error": "UrgencyLevel must be between 1 and 5"}), 400
        
        # Insert new alert
        query = """
        INSERT INTO AlertDetails (Message, SentTime, PostedBy, PostedByRole, UrgencyLevel, Protocol)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["Message"],
                data["SentTime"],
                data["PostedBy"],
                data["PostedByRole"],
                urgency_level,
                data["Protocol"]
            ),
        )
        
        db.get_db().commit()
        new_alert_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({"message": "Alert created successfully", "alert_id": new_alert_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get a specific alert with Message, SentTime, PostedBy, PostedByRole, UrgencyLevel, and Protocol
# Available to Nurse-2.3
@alerts.route("/<int:alert_id>", methods=["GET"])
def get_alert(alert_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM AlertDetails WHERE AlertID = %s", (alert_id,))
        alert = cursor.fetchone()
        
        if not alert:
            return jsonify({"error": "Alert not found"}), 404
            
        cursor.close()
        return jsonify(alert), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Acknowledge alert (sets AcknowledgedTime to NOW())
@alerts.route("/<int:alert_id>", methods=["PUT"])
def acknowledge_alert(alert_id):
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Check if alert exists
        cursor.execute("SELECT * FROM AlertDetails WHERE AlertID = %s", (alert_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Alert not found"}), 404
        
        # Get user type and ID from request
        user_type = data.get("user_type")  # "doctor" or "nurse"
        user_id = data.get("user_id")
        
        if not user_type or not user_id:
            return jsonify({"error": "user_type and user_id are required"}), 400
        
        # Set acknowledgment time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if user_type == "doctor":
            # Update or insert into AlertsDoctors
            query = """
            INSERT INTO AlertsDoctors (AlertID, DoctorID, AcknowledgedTime)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE AcknowledgedTime = VALUES(AcknowledgedTime)
            """
        elif user_type == "nurse":
            # Update or insert into AlertsNurse
            query = """
            INSERT INTO AlertsNurse (AlertID, NurseID, AcknowledgedTime)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE AcknowledgedTime = VALUES(AcknowledgedTime)
            """
        else:
            return jsonify({"error": "Invalid user_type. Must be 'doctor' or 'nurse'"}), 400
        
        cursor.execute(query, (alert_id, user_id, current_time))
        db.get_db().commit()
        cursor.close()
        
        return jsonify({"message": "Alert acknowledged successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
