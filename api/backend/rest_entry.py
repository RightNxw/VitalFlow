from flask import Flask
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.db_connection import db
from backend.simple.simple_routes import simple_routes
from backend.patient.patient_routes import patients
from backend.visit.visit_routes import visits
from backend.vital.vital_routes import vitals
from backend.condition.condition_routes import conditions
from backend.medication.medication_routes import medications
from backend.discharge.discharge_routes import discharges
from backend.insurance.insurance_routes import insurance
from backend.doctor.doctor_routes import doctors
from backend.nurse.nurse_routes import nurses
from backend.proxy.proxy_routes import proxies
from backend.message.message_routes import messages
from backend.alert.alert_routes import alerts

def create_app():
    app = Flask(__name__)

    # Configure logging
    # Create logs directory if it doesn't exist
    setup_logging(app)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # # these are for the DB object to be able to connect to MySQL.
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv(
        "DB_NAME"
    ).strip()  # Change this to your DB name

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info("create_app(): registering blueprints with Flask app object.")
    app.register_blueprint(simple_routes)
    
    # Register VitalFlow healthcare system blueprints
    app.register_blueprint(patients, url_prefix="/patient")
    app.register_blueprint(visits, url_prefix="/visit")
    app.register_blueprint(vitals, url_prefix="/vital")
    app.register_blueprint(conditions, url_prefix="/condition")
    app.register_blueprint(medications, url_prefix="/medication")
    app.register_blueprint(discharges, url_prefix="/discharge")
    app.register_blueprint(insurance, url_prefix="/insurance")
    app.register_blueprint(doctors, url_prefix="/doctor")
    app.register_blueprint(nurses, url_prefix="/nurse")
    app.register_blueprint(proxies, url_prefix="/proxy")
    app.register_blueprint(messages, url_prefix="/message")
    app.register_blueprint(alerts, url_prefix="/alert")

    # Don't forget to return the app object
    return app

def setup_logging(app):
    """
    Configure logging for the Flask application in both files and console (Docker Desktop for this project)
    
    Args:
        app: Flask application instance to configure logging for
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    ## Set up FILE HANDLER for all levels
    file_handler = RotatingFileHandler(
        'logs/api.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    # Make sure we are capturing all levels of logging into the log files. 
    file_handler.setLevel(logging.DEBUG)  # Capture all levels in file
    app.logger.addHandler(file_handler)

    ## Set up CONSOLE HANDLER for all levels
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    # Debug level capture makes sure that all log levels are captured
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    # Set the base logging level to DEBUG to capture everything
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')