from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Insurance routes
insurance = Blueprint("insurance", __name__)


# Get all insurance providers
@insurance.route("/", methods=["GET"])
def get_all_insurance():
    try:
        current_app.logger.info('Starting get_all_insurance request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Insurance")
        insurance_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(insurance_data)} insurance providers')
        return jsonify(insurance_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_insurance: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get insurance with InsuranceProvider, PolicyNumber, and Deductible
@insurance.route("/<int:insurance_id>", methods=["GET"])
def get_insurance(insurance_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Insurance WHERE InsuranceID = %s", (insurance_id,))
        insurance_info = cursor.fetchone()
        
        if not insurance_info:
            return jsonify({"error": "Insurance not found"}), 404
            
        cursor.close()
        return jsonify(insurance_info), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
