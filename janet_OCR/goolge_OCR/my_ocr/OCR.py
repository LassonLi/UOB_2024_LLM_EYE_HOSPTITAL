
# Imports the Google Cloud client library
from google.cloud import vision
import io
import os
import json

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

    def get_dict_from_dataset(self, directory_path: str) -> dict:
        "read all dataset and save it to a dict (ex.{filename: result_string}"
        results = {}

        # Get all files in the directory
        for filename in os.listdir(directory_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Construct the full file path
                file_path = os.path.join(directory_path, filename)
                text = self.run_quickstart(file_path)
                results[filename] = text

        return results

    def calculate_score(self, detected_text: str, correct_text: str) -> float:
        score = 0.0

        # calculate logic

        return score



    def calculate_score_from_dataset(self, image_directory_path: str, annotation_directory_path: str) -> float:

        total_score = 0.0
        num_images = 0

        for filename in os.listdir(image_directory_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_file_path = os.path.join(image_directory_path, filename)

                # remove file extension(ex. .png/.json) from filename
                filename_without_extension = os.path.splitext(filename)[0]

                json_file_path = os.path.join(annotation_directory_path, filename_without_extension + '.json')

                if os.path.isfile(json_file_path):
                    # load "correct answer" from json
                    with open(json_file_path, 'r') as f:
                        correct_answer = json.load(f)
                        correct_text = correct_answer.get(filename)


                detect_text = self.run_quickstart(image_file_path)


                if correct_text is not None:
                    # compare origin text and ocr text --> get a score
                    score = self.calculate_score(detect_text, correct_text)
                    total_score += score
                    num_images += 1

        # calculate the average score
        average_score: float = total_score / num_images if num_images > 0 else 0.0

        return average_score




if __name__ == "__main__":
    detector = OCRDetector()
    text = detector.run_quickstart("assests/Referral_letter_example.jpg")
    print(text)