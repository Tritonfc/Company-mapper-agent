from googleapiclient.discovery import build
from .gmail_auth import get_credentials

creds = get_credentials()


def get_gmail_service():    
    gmail = build("gmail", "v1", credentials=creds)

    request = {
    'labelIds': ['INBOX'],
    'topicName': 'projects/gmail-tracking-491020/topics/Incoming-emails',
    'labelFilterBehavior': 'INCLUDE'
    }

    response = gmail.users().watch(userId='me', body=request).execute()
    print("Watch set up successfully!")
    print(f"History ID: {response.get('historyId')}")
    print(f"Expiration: {response.get('expiration')}")
    return response