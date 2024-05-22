import os.path
from google.oauth2.credentials import Credentials#handles oauth credentials
from google_auth_oauthlib.flow import InstalledAppFlow #manages the outh2 autorization flow
from google.auth.transport.requests import Request #provide http transport for makin request
from googleapiclient.discovery import build # build gmail api service object
# initially used https://www.googleapis.com/auth/gmail.modify scope but due to an error had to change it to this one
SCOPES = ['https://mail.google.com/'] #access scopes the link allows the script to read modify and delete emails

def authenticate_gmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time. 
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:  # firstly see if token.js where the credneitals are stored exists if it doesnt exist then put the credentials in token.js after creating it
            #if the credits arent valid or have expired then send request else use the credentials in credentials.json
            #then load that into token.js
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def delete_unopened_emails(service, sender_email): #service is the gmail api service object
    # Get list of unread messages from a specific sender
    query = f'from:{sender_email} is:unread'# to find unread emails from the sender
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
        return
#else part of the above if is below
    for message in messages:#iterate trrough each msg and delete one by one
        msg_id = message['id']
        print(f'Deleting message ID: {msg_id}')
        service.users().messages().delete(userId='me', id=msg_id).execute()

def main():
    sender_email = 'notifync@naukri.com'  # The sender's email address
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    delete_unopened_emails(service, sender_email)

if __name__ == '__main__':
    main()
