from calendar import Calendar
from recognizer import Recognizer
import extractor
import datetime
import os
from dotenv import load_dotenv


def main(photo):

    try:
        load_dotenv()

        region_name = os.getenv('REGION_NAME')
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        base_path = os.getenv('BASE_PATH')

        recognizer_instance = Recognizer(region_name, aws_access_key_id,
                                          aws_secret_access_key, base_path)
        text_detected = recognizer_instance.detect_text(photo)
        if text_detected:
            print("Text detected: " + str(text_detected))
        else:
            print("No text detected.")

        extracted_datetime = None
        extracted_number = ""
        extracted_details = extractor.extract_details(text_detected)
        if extracted_details:
            print("extracted_details: " + str(extracted_details))
            if len(extracted_details[0]) > 0:
                extracted_datetime = extracted_details[0]
            if len(extracted_details[1]) > 0:
                extracted_number = extracted_details[1]
        else:
            print("No details detected.")
        
        
        if extracted_datetime:
            description = f'Card with number: {extracted_number} expiring on {extracted_datetime}'
            start_datetime = extracted_datetime
            end_datetime = extracted_datetime.date() + datetime.timedelta(hours=23, minutes=59)

            print(f'description: {description} ,
            start_datetime: {start_datetime} ,
            end_datetime: {end_datetime}')

            # calendar_id = os.getenv('CALENDAR_ID')     
            # calendar_instance = Calendar(calendar_id)
            # event_id = calendar_instance.create_event(description, start_datetime, end_datetime)
            # print("Event created with ID:", event_id)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    photo = input('photo-name: ')
    main(photo)
