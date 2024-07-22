from flask import Flask

import config
from config import Config
import os


# Create and initialise Flask application instance
def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Set up configuration settings for the Flask app
    app.config.from_object(Config)

    #Print details of app.config
    print(app.config["CREDENTIAL_PATH"])

    # Set up the Google Cloud credentials environmnet variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config["CREDENTIAL_PATH"]
    os.environ["GOOGLE_CLOUD_PROJECT"] = "ocr-project-427217"

    # Ensure the uploads directory exists within the static folder
    upload_path = os.path.join(app.static_folder, app.config["UPLOAD_FOLDER"])
    os.makedirs(upload_path, exist_ok=True)

    # Import thr routes module
    from . import routes
    # Register the blueprint with the Flask app instance
    # so all routes/handlers defined in the blueprint available in the main application
    app.register_blueprint(routes.bp)

    return app

