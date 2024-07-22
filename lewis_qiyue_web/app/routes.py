import csv
import traceback
from io import StringIO

from flask import Blueprint, render_template, request, jsonify, current_app, url_for
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
def upload_single():
    if 'image' not in request.files:
        return render_template(HTML_FILE, single_error="No file part")

    file = request.files['image']
    logging.debug(f"Received file: {file.filename}")

    if file.filename == '':
        logging.error("No selected file")
        return render_template(HTML_FILE, single_error="No selected file")

    if file and check_file_extension(file.filename):
        # Sanitise the file name
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'], filename)
        logging.debug(f"Saving file to: {file_path}")
        file.save(file_path)

        # Pass the filepath to OCR
        detector = OCRDetector()
        try:
            text = detector.run_quickstart(file_path)
            logging.debug("OCR processing complete")
            #display image_url on the website
            image_url = url_for('static',filename='uploads/' + filename)
            return render_template(HTML_FILE, text=text, image_url=image_url)
        except Exception as e:
            logging.error(f"Error during OCR processing: {e}")
            return render_template(HTML_FILE, single_error=str(e))

    logging.error("Invalid file type")
    return render_template(HTML_FILE, single_error="Invalid file type")

@bp.route('/upload_folder', methods=['POST'])
def upload_folder():
    if 'folder' not in request.files:
        logging.error("No folder part in the request")
        return render_template(HTML_FILE, folder_error="No folder part in the request")

    files = request.files.getlist('folder')
    if not files:
        logging.error("No selected folder")
        return render_template(HTML_FILE, folder_error="No selected folder")

    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Filename', 'Extracted Text'])

    detector = OCRDetector()

    for file in files:
        if file and check_file_extension(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.static_folder, current_app.config["UPLOAD_FOLDER"], filename)
            logging.debug(f"Saving file to: {file_path}")
            file.save(file_path)

            try:
                text = detector.run_quickstart(file_path)
                csv_writer.writerow([filename, text])
            except Exception as error:
                logging.error(f"Error during OCR processing: {error}")
                csv_writer.writerow([filename, f"Error: {error}"])
        else:
            logging.error(f"Invalid file type for file: {file.filename}")
            csv_writer.writerow([file.filename, "Error: Invalid file type"])

    csv_filename = "result.csv"
    csv_path = os.path.join(current_app.static_folder, 'csv', csv_filename)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open (csv_path, 'w', newline = '') as csv_file:
        csv_file.write(csv_data.getvalue())

    logging.debug(f"Saving file to: {csv_path}")
    return render_template(HTML_FILE, csv_file=csv_filename)






def check_file_extension(filename):
    ALLOWED_TYPE = ('png', 'jpg', 'jpeg', 'pdf')

    # Check if the filename is valid
    if '.' in filename and filename.rsplit('.',1)[-1].lower() in ALLOWED_TYPE:
        return True
    else:
        return False
