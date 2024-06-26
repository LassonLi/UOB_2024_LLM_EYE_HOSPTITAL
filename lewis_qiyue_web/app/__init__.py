from flask import Flask
from config import Config
import os


# Create and initialise Flask application instance
def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Set up configuration settings for the Flask app
    app.config.from_object(Config)

    # Set up the Google Cloud credentials environmnet variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config["GOOGLE_APPLICATION_CREDENTIALS"]

    # Import thr routes module
    from . import routes
    # Register the blueprint with the Flask app instance
    # so all routes/handlers defined in the blueprint available in the main application
    app.register_blueprint(routes.bp)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    return app

