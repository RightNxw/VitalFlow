from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Message routes
messages = Blueprint("messages", __name__)


# Get messages for a user (accessible via MessagePatients, MessageDoctor, or MessageNurse)
# Available to Patient-3.1, Doctor-1.5, Doctor-1.6, Nurse-2.6
@messages.route("/messages", methods=["GET"])
def get_messages():
    try:
        current_app.logger.info('Starting get_messages request')
        cursor = db.get_db().cursor()
        
        # Get query parameters for filtering by user type and ID
        user_type = request.args.get("user_type")  # "patient", "doctor", or "nurse"
        user_id = request.args.get("user_id")
        
        if not user_type or not user_id:
            return jsonify({"error": "user_type and user_id parameters are required"}), 400
        
        # Get messages based on user type
        if user_type == "patient":
            query = """
            SELECT md.* FROM MessageDetails md
            JOIN MessagePatients mp ON md.MessageID = mp.MessageID
            WHERE mp.PatientID = %s
            ORDER BY md.SentTime DESC
            """
        elif user_type == "doctor":
            query = """
            SELECT md.* FROM MessageDetails md
            JOIN MessageDoctor mdoc ON md.MessageID = mdoc.MessageID
            WHERE mdoc.DoctorID = %s
            ORDER BY md.SentTime DESC
            """
        elif user_type == "nurse":
            query = """
            SELECT md.* FROM MessageDetails md
            JOIN MessageNurse mn ON md.MessageID = mn.MessageID
            WHERE mn.NurseID = %s
            ORDER BY md.SentTime DESC
            """
        else:
            return jsonify({"error": "Invalid user_type. Must be 'patient', 'doctor', or 'nurse'"}), 400
        
        cursor.execute(query, (user_id,))
        messages_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(messages_data)} messages for {user_type} {user_id}')
        return jsonify(messages_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_messages: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Create message
# Available to Patient-3.3, Doctor-1.5, Doctor-1.6, Nurse-2.6
@messages.route("/messages", methods=["POST"])
def create_message():
    try:
        data = request.get_json()
        cursor = db.get_db().cursor()
        
        # Validate required fields
        required_fields = ["Message", "PostedBy", "PostedByRole"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Insert new message
        query = """
        INSERT INTO MessageDetails (MessageTitle, Message, SentTime, PostedBy, PostedByRole)
        VALUES (%s, %s, NOW(), %s, %s)
        """
        cursor.execute(
            query,
            (
                data.get("MessageTitle", ""),
                data["Message"],
                data["PostedBy"],
                data["PostedByRole"]
            ),
        )
        
        db.get_db().commit()
        new_message_id = cursor.lastrowid
        
        # Handle recipient assignment based on recipient type and ID
        recipient_type = data.get("RecipientType")
        recipient_id = data.get("RecipientID")
        
        if recipient_type and recipient_id:
            if recipient_type == "patient":
                cursor.execute(
                    "INSERT INTO MessagePatients (MessageID, PatientID) VALUES (%s, %s)",
                    (new_message_id, recipient_id)
                )
            elif recipient_type == "doctor":
                cursor.execute(
                    "INSERT INTO MessageDoctor (MessageID, DoctorID) VALUES (%s, %s)",
                    (new_message_id, recipient_id)
                )
            elif recipient_type == "nurse":
                cursor.execute(
                    "INSERT INTO MessageNurse (MessageID, NurseID) VALUES (%s, %s)",
                    (new_message_id, recipient_id)
                )
            
            db.get_db().commit()
        
        cursor.close()
        
        return jsonify({"message": "Message created successfully", "message_id": new_message_id}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get a specific message with Message, SentTime, PostedBy, and PostedByRole
@messages.route("/messages/<int:message_id>", methods=["GET"])
def get_message(message_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM MessageDetails WHERE MessageID = %s", (message_id,))
        message = cursor.fetchone()
        
        if not message:
            return jsonify({"error": "Message not found"}), 404
            
        cursor.close()
        return jsonify(message), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
