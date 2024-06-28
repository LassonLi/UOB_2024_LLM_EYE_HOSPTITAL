import os

OCR_CREDENTIAL = "Janet_OCR_credentials.json"


class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_SIZE = 32 * 1024 * 1024  #32MB limit for upload files
    GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.getcwd(), 'instance', OCR_CREDENTIAL)
