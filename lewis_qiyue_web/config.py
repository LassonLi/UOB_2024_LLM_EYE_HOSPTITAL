import os

OCR_CREDENTIAL = "Janet_OCR_credential.json"


class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_SIZE = 32 * 1024 * 1024  #32MB limit for upload files
    CREDENTIAL_PATH = os.path.join(os.getcwd(), 'instance', OCR_CREDENTIAL)
