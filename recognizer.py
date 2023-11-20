import boto3
import os


class Recognizer:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, base_path=""):

        # Create an AWS session
        session = boto3.Session(
            region_name=region_name,  # Replace with the desired AWS region
            aws_access_key_id=aws_access_key_id,  # Replace with your AWS access key ID
            aws_secret_access_key=aws_secret_access_key,  # Replace with your AWS secret access key
            # aws_session_token='your_session_token'  # Replace with your AWS session token (optional)
        )

        self.base_path = base_path

        # Initialize the desired AWS service client using the session
        self.client = session.client('rekognition')

        # Amazon Textract client
        # self.textract = session.client('textract')



    """
    Detects text in an image using Amazon Rekognition and Amazon Textract.

    :param photo: The name of the photo file to be processed.
    :type photo: str
    :param bucket: The name of the S3 bucket where the photo is stored. If not provided, the photo will be loaded from the local file system.
    :type bucket: str, optional
    :param base_path: The base path of the local file system where the photo is stored. Only used if bucket is not provided.
    :type base_path: str, optional
    :return: The number of text detections found in the image.
    :rtype: int
    """
    def detect_text(self, photo, bucket=None, base_path=None):

        if base_path is None:
            base_path = self.base_path

        if bucket and bucket!="":
            response = self.client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})
        else:
            # Load the image from local file as bytes
            with open(os.path.join(base_path, photo), 'rb') as image_file:
                image_bytes = image_file.read()
            response = self.client.detect_text(Image={'Bytes': image_bytes})

        try:
            textDetections = response['TextDetections']
            # print(textDetections)
            print('Detected text\n----------')
            detected_text = []
            for text in textDetections:
                if text['Type'] == "LINE" and text['Confidence']>50:
                    print('Detected text:' + text['DetectedText'])
                    print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
                    detected_text.append(text['DetectedText'])
                    # print('Id: {}'.format(text['Id']))
                    # if 'ParentId' in text:
                    #     print('Parent Id: {}'.format(text['ParentId']))
                    # print('Type:' + text['Type'])
        
            # Call Amazon Textract
            # response_textract = self.textract.detect_document_text(Document={'Bytes': image_bytes})
            # print("======== Textract response =========")
            # # Print detected text
            # for item in response_textract["Blocks"]:
            #     if item["BlockType"] == "LINE":
            #         print ('\033[94m' +  item["Text"] + '\033[0m')

            return detected_text
        except Exception as e:
            print(e)
            return None





def main():
    while True:
        bucket = input('bucket-name: ')
        photo = input('photo-name: ')
        recognizer_instance = Recognizer()
        text_detected = recognizer_instance.detect_text(photo, bucket)
        if text_detected:
            print("Text detected: " + str(text_detected))
        else:
            print("No text detected.")

if __name__ == "__main__":
    main()