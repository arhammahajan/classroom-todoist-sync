import requests
r = requests.get('https://classroom.googleapis.com/v1/courses', )
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly", "https://www.googleapis.com/auth/classroom.coursework.me", "https://www.googleapis.com/auth/classroom.announcements"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        results = service.courses().list().execute()
        print(results)
        courses = results.get("courses", [])

        if not courses:
            print("No courses found.")
            return

        print("Courses:")
        for course in courses:
            print(course["name"])
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()