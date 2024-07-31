import os
import ctypes

import pytesseract
from PIL import Image

class TesseractOCR:

    def __init__(self, executable_path):
        self.executable_path = executable_path
        pytesseract.pytesseract.tesseract_cmd = self.executable_path

    def perform_ocr(self, image_path):
        image = Image.open(image_path)

        return pytesseract.image_to_string(image)



if __name__ == "__main__":
    ocr = TesseractOCR('/opt/homebrew/Cellar/tesseract/5.4.1/bin/tesseract')
    result_string = ocr.perform_ocr("../assests/Referral_letter_example.jpg")
    print(result_string)


