from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for Proxy routes
proxies = Blueprint("proxies", __name__)


# Get all proxies
@proxies.route("/proxies", methods=["GET"])
def get_all_proxies():
    try:
        current_app.logger.info('Starting get_all_proxies request')
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Proxy")
        proxies_data = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(proxies_data)} proxies')
        return jsonify(proxies_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_proxies: {str(e)}')
        return jsonify({"error": str(e)}), 500


# Get a specific proxy with FirstName, LastName, and Relationship
@proxies.route("/proxies/<int:proxy_id>", methods=["GET"])
def get_proxy(proxy_id):
    try:
        cursor = db.get_db().cursor()
        
        cursor.execute("SELECT * FROM Proxy WHERE ProxyID = %s", (proxy_id,))
        proxy = cursor.fetchone()
        
        if not proxy:
            return jsonify({"error": "Proxy not found"}), 404
            
        cursor.close()
        return jsonify(proxy), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get all patients where Proxy.PatientID matches
# Available to Proxy-4.1 through 4.6
@proxies.route("/proxies/<int:proxy_id>/patients", methods=["GET"])
def get_proxy_patients(proxy_id):
    try:
        cursor = db.get_db().cursor()
        
        # Check if proxy exists
        cursor.execute("SELECT * FROM Proxy WHERE ProxyID = %s", (proxy_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Proxy not found"}), 404
        
        # Get all patients for this proxy
        query = """
        SELECT p.* FROM Patient p
        JOIN Proxy pr ON p.PatientID = pr.PatientID
        WHERE pr.ProxyID = %s
        """
        cursor.execute(query, (proxy_id,))
        patients = cursor.fetchall()
        cursor.close()
        
        return jsonify(patients), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
