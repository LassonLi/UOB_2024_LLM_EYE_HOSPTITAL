from venv import logger
import boto3


class ClientError:
    pass

class AWSTextDetector:
    """Encapsulates Textract functions."""

    def __init__(self):
        """
        Initializes the Textract client, S3 resource, and SQS resource.
        """
        session = boto3.Session()
        self.textract_client = session.client('textract')
        self.s3_resource = session.resource('s3')
        self.sqs_resource = session.resource('sqs')


    def detect_file_text(self, *, document_file_name=None, document_bytes=None):
        """
        Detects text elements in a local image file or from in-memory byte data.
        The image must be in PNG or JPG format.

        :param document_file_name: The name of a document image file.
        :param document_bytes: In-memory byte data of a document image.
        :return: The response from Amazon Textract, including a list of blocks
                 that describe elements detected in the image.
        """
        if document_file_name is not None:
            with open(document_file_name, 'rb') as document_file:
                document_bytes = document_file.read()
        try:
            response = self.textract_client.detect_document_text(
                Document={"Bytes": document_bytes}
            )
            logger.info("Detected %s blocks.", len(response["Blocks"]))


            # Extract the text from the response
            result_string = ""
            for block in response['Blocks']:
                if block['BlockType'] in ['WORD', 'LINE']:
                    result_string += block['Text'] + " "

                    # if block['Text'].endswith('.'):
                    #     result_string += "\n"
                    # else:
                    #     result_string += " "

            return result_string

        except ClientError:
            logger.exception("Couldn't detect text.")
            raise



if __name__ == "__main__":
    aws_text_detector = AWSTextDetector()
    response = aws_text_detector.detect_file_text(document_file_name='assests/Referral_letter_example.jpg')
    print(response)