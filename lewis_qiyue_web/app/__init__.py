import os
import sys
from flask import Flask

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    print(f"Config CREDENTIAL_PATH: {app.config['CREDENTIAL_PATH']}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config["CREDENTIAL_PATH"]
    os.environ["GOOGLE_CLOUD_PROJECT"] = "ocr-project-427217"

    upload_path = os.path.join(app.static_folder, app.config["UPLOAD_FOLDER"])
    os.makedirs(upload_path, exist_ok=True)
    print(f"Upload path created: {upload_path}")

    from app import routes
    app.register_blueprint(routes.bp)

    return app

if __name__ == '__main__':
    print("Starting Flask application...")
    app = create_app()
    print("Flask application created")
    app.run(host='0.0.0.0', port=5000)
