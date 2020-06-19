from abc import ABCMeta, abstractmethod
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class BaseService(metaclass=ABCMeta):

    @abstractmethod
    def build(self):
        return


class BaseGoogleService(BaseService):
    token_name = ''
    scopes = []

    def __init__(self, credentials_path, api, version):
        super(BaseGoogleService, self).__init__()
        self.credentials_path = credentials_path
        self.api = api
        self.version = version
        self.service = self.build()

    def build(self):
        token_name = self.__class__.token_name

        creds = None
        if os.path.exists(token_name):
            with open(token_name, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.__class__.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_name, 'wb') as token:
                pickle.dump(creds, token)

        return build(self.api, self.version, credentials=creds)

    def get(self):
        return self.service
