
# Imports the Google Cloud client library
from google.cloud import vision
import io

class OCRDetector:

    global float

    def __init__(self):
        # Instantiates a client
        self.client = vision.ImageAnnotatorClient()

    def run_quickstart(self, file_path: str) -> str:
        """Provides a quick start example for Cloud Vision."""

        # Instantiates a client
        # client = vision.ImageAnnotatorClient()

        # The path of the image file to annotate
        # file_path = "assests/Referral_letter_example.jpg"

        # Loads the image into memory
        with io.open(file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Performs label detection on the image file
        response = self.client.text_detection(image=image)
        texts = response.text_annotations

        return texts[0].description



if __name__ == "__main__":
    detector = OCRDetector()
    text = detector.run_quickstart("assests/Referral_letter_example.jpg")
    # print(text)

    detector.calculate_score_from_dataset("/Users/lishin/Desktop/Bristol/Summer Project/UOB_2024_LLM_EYE_HOSPTITAL/janet_OCR/dataset/training_data")