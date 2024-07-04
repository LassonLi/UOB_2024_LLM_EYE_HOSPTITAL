import os
import json
from my_ocr import OCRDetector
from my_aws_ocr import AWSTextDetector
from my_tesseract_ocr import TesseractOCR
from jiwer import wer

class Eval:

    def __init__(self):
        self.google_detector = OCRDetector()
        self.aws_detector = AWSTextDetector()
        self.tesseract_detector = TesseractOCR("/opt/homebrew/Cellar/tesseract/5.4.1/bin/tesseract")


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


    def getSortedText(self, annotation_file, tolerance = 5) -> str:

        data = json.load(annotation_file)
        forms = data.get('form', [])

        # [先按照y排列]
        # 按 "y座標" 排列 form(array) 裡面的element (因為要 "由上到下 由左而右") ([1] --> y軸高度)
        form_sorted_by_y = sorted(forms, key=lambda i: i['box'][1])

        # 按照 相同/類似高度 分類的子array (group裡是 一個一個 "高度不同" 的子array)(array裡可能會有 1個/多個 element)
        group = []
        similar_height_subgroup = []

        # 從 第0項 開始，拿 他的y 來跟接下來幾項比較 （高度誤差範圍內 --> 放到同個subgroup）
        current_y = form_sorted_by_y[0]['box'][1]

        for item in form_sorted_by_y:
            y = item['box'][1]
            if abs(y - current_y) <= tolerance:
                similar_height_subgroup.append(item)
            else:
                # 放入 "前一個"subgroup
                group.append(similar_height_subgroup)
                # new 一個 "新的subgroup" 放入item(element)
                similar_height_subgroup = [item]
                current_y = y

        #把 "最後一個subgroup" 放進group
        if similar_height_subgroup:
            group.append(similar_height_subgroup)

        # [按照x排列]
        # sorted_text(array) 裡 是一個個 "string" (string --> subgroup裡的item 按照x排列 的text)
        sorted_text = []

        for subgroup in group:
            # ([0] --> x軸)
            for item in sorted(subgroup, key=lambda i: i['box'][0]):
                if 'text' in item and item['text']:
                    sorted_text.append(item['text'])

        return ' '.join(sorted_text)



    def calculate_score(self, detected_text: str, correct_text: str) -> float:
        # calculate logic (error = wer(reference, hypothesis))
        error = wer(correct_text, detected_text)

        return error



    def calculate_score_from_dataset(self, detector_type: str, base_directory_path: str) -> float:

        total_error = 0.0
        num_images = 0

        image_directory_path = os.path.join(base_directory_path, 'images')
        annotation_directory_path = os.path.join(base_directory_path, 'annotations')

        for filename in os.listdir(image_directory_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_file_path = os.path.join(image_directory_path, filename)

                # remove file extension(ex. .png/.json) from filename
                filename_without_extension = os.path.splitext(filename)[0]

                json_file_path = os.path.join(annotation_directory_path, filename_without_extension + '.json')

                if os.path.isfile(json_file_path):
                    # load "correct answer" from json
                    with open(json_file_path, 'r') as f:

                        groundtruth = self.getSortedText(f)

                    # print(f"Image file:\n {image_file_path}")
                    # print(f"Annotation file: {json_file_path}")
                    # print(f"Correct text: {groundtruth}")

                if detector_type == "google" :
                    detect_text = self.google_detector.run_quickstart(image_file_path)
                elif detector_type == "aws":
                    detect_text = self.aws_detector.detect_file_text(document_file_name=image_file_path)
                else:
                    detect_text = self.tesseract_detector.perform_ocr(image_file_path)

                # print(f"Detected text: {detect_text}")


                if groundtruth is not None:
                    # compare origin text and ocr text --> get a score
                    error = self.calculate_score(detect_text, groundtruth)
                    total_error += error
                    num_images += 1

        # calculate the average score (error越低越準確）
        average_error: float = total_error / num_images if num_images > 0 else 0.0

        return average_error


if __name__ == "__main__":
    eval = Eval()

    google_average_error = eval.calculate_score_from_dataset("google", "/Users/lishin/Desktop/Bristol/Summer Project/UOB_2024_LLM_EYE_HOSPTITAL/janet_OCR/dataset/training_data")
    print(google_average_error)

    aws_average_error = eval.calculate_score_from_dataset("aws",
                                      "/Users/lishin/Desktop/Bristol/Summer Project/UOB_2024_LLM_EYE_HOSPTITAL/janet_OCR/dataset/training_data")
    print(aws_average_error)
    
    tesseract_average_error = eval.calculate_score_from_dataset("tesseract",
                                      "/Users/lishin/Desktop/Bristol/Summer Project/UOB_2024_LLM_EYE_HOSPTITAL/janet_OCR/dataset/training_data")
    print(tesseract_average_error)