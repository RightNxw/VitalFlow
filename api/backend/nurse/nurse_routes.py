from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Nurse routes
nurses = Blueprint("nurses", __name__)


# Get all nurses
# Available to Proxy-4.6
@nurses.route("/nurses", methods=["GET"])
def get_all_nurses():
    try:
        current_app.logger.info('Starting get_all_nurses request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Nurse")
        nurses_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(nurses_data)} nurses')
        return jsonify(nurses_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_nurses: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get a specific nurse with FirstName and LastName
# Available to Proxy-4.6
@nurses.route("/nurses/<int:nurse_id>", methods=["GET"])
def get_nurse(nurse_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Nurse WHERE NurseID = %s", (nurse_id,))
        nurse = cursor.fetchone()
        
        if not nurse:
            return jsonify({"error": "Nurse not found"}), 404
            
        cursor.close()
        return jsonify(nurse), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
