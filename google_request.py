from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
import uuid

#GD Auth
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def build_service_request():
    '''
    Function to build google drive api service to make request.
    '''
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v2', credentials=creds)
    return service



def request_doc_modification():
    '''
    Function to request for file modifications.
    '''
    service = build_service_request()

    results = service.files().get(fileId="1p4Dp14a_85cnExpDxgujivCAqA7fn9BWpiBRmAA5CRg").execute()

    last_doc_modified = None    
    modified_date = results['modifiedDate']
    doc_response = None


    # Get last_doc_modified date from 'dateModified.txt' if it exists.
    if os.path.exists('dateModified.txt'):
        with open('dateModified.txt', 'r') as date:
            last_doc_modified = date.read()
    # Write to 'dateModified.txt' if it doesn't exist for future comparison .
    if not last_doc_modified or last_doc_modified < modified_date:    
        if last_doc_modified is not None:
            doc_response = f"Document <{results['alternateLink']}|*'{results['title']}'*> has been modified."
            print('Modified Doc')
            
        with open('dateModified.txt','w') as date:
            date.write(modified_date)

    elif last_doc_modified == modified_date:
        doc_response = f"Document is *not* modified"
        
        print('Nothing')
    
    return doc_response


    
        


    