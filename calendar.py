import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar.events']

token_file = os.path.join("env", "token.json")
client_secret_file = os.path.join("env", "client_secret_web.json")

class Calendar:
    def __init__(self, calendar_id):

        self.calendar_id = calendar_id

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())

        try:
            # Build the calendar service
            self.service = build('calendar', 'v3', credentials=creds)

        except HttpError as error:
            print('An error occurred: %s' % error)


    def create_event(self, summary, start_datetime, end_datetime, calendarId=None):
        if calendarId is None:
            calendarId = self.calendar_id
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Asia/Kolkata',
            },
        }
        event = self.service.events().insert(calendarId=calendarId, body=event).execute()
        return event['id']


    # start_datetime = datetime.datetime.strptime("2023-12-30 00:00", "%Y-%m-%d %H:%M")
    # end_datetime = datetime.datetime.strptime("2023-12-30 23:59", "%Y-%m-%d %H:%M")
    # create_event("summary", start_datetime, end_datetime, self.calendar_id)


def main():
    summary = input("Enter event summary: ")
    start_datetime = datetime.datetime.strptime(input("Enter start datetime (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    end_datetime = datetime.datetime.strptime(input("Enter end datetime (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    
    calendar_instance = Calendar()
    event_id = calendar_instance.create_event(summary, start_datetime, end_datetime)
    print("Event created with ID:", event_id)

if __name__ == '__main__':
    main()