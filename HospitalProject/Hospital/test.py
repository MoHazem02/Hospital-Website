import os.path
import datetime as dt
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = Credentials.from_authorized_user_file("Hospital Credentials API.json")

    flow = InstalledAppFlow.from_client_secrets_file("Hospital Credentials API.json", SCOPES)
    
    try:
        pass
    except HttpError as error:
        print(f"an error occurred {error}")