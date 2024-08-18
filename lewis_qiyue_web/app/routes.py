import csv
import traceback
from io import StringIO
from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
import os
from my_ocr import OCRDetector
import logging
import boto3
import json
import re

HTML_FILE = "webpage.html"
logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('main', __name__)

# Set AWS region and end point
region_name = 'eu-west-2'  # Example，'us-west-2'
endpoint_name = 'gemma'

# Initialise SageMaker client
sagemaker_client = boto3.client('sagemaker-runtime', region_name=region_name)

instruction = """Synonyms: ["Papilledema","Swollen discs","Indistinct margins","Blurred disc margins","Suspicious discs","Disc swelling","Optic nerve swelling"]
PseudoSynonyms: ["Pseudopapilledema","Drusen","Tilted disc","Anomalous discs"]

Role : You are a experienced doctor who have memory of electronic medical records related to many diseases.
Instruction : please extract the referral content from the following referral letter separated by ###. 
output your result directly in format: "is_Papilledema": boolean, "referral_content": "".
Rule For is_Papilledema : If the referral letter contains one of words in Synonyms, then is_Papilledema = true; If the letter contains words in PseudoSynonyms or doesn't contain words in Synonyms, then is_Papilledema = False.
Rule For referral_content : this content should be a whole paragraph which tells Patient need referral. If the referral_letter contains this content, you should include it. If the letter doesn't contain related information, then it should be null."""

def call_sagemaker(whole_letter):
    prompt = f"{instruction}\n\n###\n\n{whole_letter}\n\n###"
    payload_dict = {
        'inputs': prompt,
        'parameters': {'max_new_tokens': 256}
    }

    # Serialise input data to JSON String
    payload = json.dumps(payload_dict)

    # Invoke SageMaker Endpoint
    response = sagemaker_client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',  # Choose the appropriate content type based on your model's requirements
        Body=payload
    )

    # Parse/decode the response
    result = json.loads(response['Body'].read().decode())

    # Extract the content from referral_content
    generated_text = result[0]["generated_text"]
    referral_content_match = re.search(r'"referral_content":\s*"([^"]+)"', generated_text)

    if referral_content_match:
        referral_content = referral_content_match.group(1)
    else:
        referral_content = ""

    return referral_content

@bp.route('/')
def index():
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
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'], filename)
        logging.debug(f"Saving file to: {file_path}")
        file.save(file_path)

        detector = OCRDetector()
        try:
            text = detector.run_quickstart(file_path)
            logging.debug("OCR processing complete")
            image_url = url_for('static', filename='uploads/' + filename)

            # Call SageMaker
            referral_content = call_sagemaker(text)
            logging.debug(f"SageMaker response: {referral_content}")

            return render_template(HTML_FILE, text=referral_content, image_url=image_url)
        except Exception as e:
            logging.error(f"Error during OCR or SageMaker processing: {e}")
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
    csv_writer.writerow(['Filename', 'Extracted Text', 'SageMaker Result'])

    detector = OCRDetector()

    for file in files:
        if file and check_file_extension(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.static_folder, current_app.config["UPLOAD_FOLDER"], filename)
            logging.debug(f"Saving file to: {file_path}")
            file.save(file_path)

            try:
                text = detector.run_quickstart(file_path)
                logging.debug("OCR processing complete")

                # Call SageMaker
                referral_content = call_sagemaker(text)
                logging.debug(f"SageMaker response: {referral_content}")

                csv_writer.writerow([filename, text, referral_content])
            except Exception as error:
                logging.error(f"Error during OCR or SageMaker processing: {error}")
                csv_writer.writerow([filename, f"Error: {error}"])
        else:
            logging.error(f"Invalid file type for file: {file.filename}")
            csv_writer.writerow([file.filename, "Error: Invalid file type"])

    csv_filename = "result.csv"
    csv_path = os.path.join(current_app.static_folder, 'csv', csv_filename)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='') as csv_file:
        csv_file.write(csv_data.getvalue())

    logging.debug(f"Saving file to: {csv_path}")
    return render_template(HTML_FILE, csv_file=csv_filename)

def check_file_extension(filename):
    ALLOWED_TYPE = ('png', 'jpg', 'jpeg', 'pdf')
    if '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_TYPE:
        return True
    else:
        return False
