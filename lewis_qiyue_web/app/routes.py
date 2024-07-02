from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from my_ocr import OCRDetector
import logging

HTML_FILE = "webpage.HTML"
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('main', __name__)
@bp.route('/')
def index():
    #render HTML file saved in templates
    return render_template(HTML_FILE)

@bp.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return render_template(HTML_FILE, error="No file part")

    file = request.files['image']
    logging.debug(f"Received file: {file.filename}")

    if file.filename == '':
        logging.error("No selected file")
        return render_template(HTML_FILE, error="No selected file")

    if file and check_file_extension(file.filename):
        # Sanitise the file name
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        logging.debug(f"Saving file to: {file_path}")
        file.save(file_path)

        # Pass the filepath to OCR
        detector = OCRDetector()
        try:
            text = detector.run_quickstart(file_path)
            logging.debug("OCR processing complete")
            return render_template(HTML_FILE, text=text)
        except Exception as e:
            logging.error(f"Error during OCR processing: {e}")
            return render_template(HTML_FILE, error=str(e))

    logging.error("Invalid file type")
    return render_template(HTML_FILE, error="Invalid file type")


def check_file_extension(filename):
    ALLOWED_TYPE = ('png', 'jpg', 'jpeg', 'pdf')

    # Check if the filename is valid
    if '.' in filename and filename.rsplit('.',1)[-1].lower() in ALLOWED_TYPE:
        return True
    else:
        return False
