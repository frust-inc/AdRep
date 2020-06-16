import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from .base import BaseWriter

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


class GoogleSpreadSheetWriter(BaseWriter):
    def __init__(self, config=None):
        super(GoogleSpreadSheetWriter, self).__init__(config=config)

        if "SHEET_ID" in config:
            self.sheet_id = config["SHEET_ID"]
        else:
            raise ValueError("SHEET_ID must be specified.")

        if "SHEET_NAME" in config:
            self.sheet_name = config["SHEET_NAME"]
        else:
            raise ValueError("SHEET_NAME must be specified.")

        if "SHEET_RANGE" in config:
            self.sheet_range = "{}!{}".format(config["SHEET_NAME"], config["SHEET_RANGE"])
        else:
            raise ValueError("SHEET_RANGE must be specified.")

        if "CREDENTIALS_PATH" in config:
            self.credentials_path = config["CREDENTIALS_PATH"]
        else:
            raise ValueError("CREDENTIALS_PATH must be specified.")

        if "FIELDNAMES" in config:
            self.fieldnames = config["FIELDNAMES"]
        else:
            raise ValueError("FIELDNAMES must be specified.")

    def _build_service(self):
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
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('sheets', 'v4', credentials=creds)

    def _format(self, reports):
        formatted = []
        for report in reports:
            # TODO: data validation
            values = report.to_dict()
            formatted.append([values[header] for header in self.fieldnames])
        return formatted


    def write(self, reports):
        value_input_option = 'USER_ENTERED'
        insert_data_option = 'OVERWRITE'

        service = self._build_service()

        # TODO: process if beginning of the month
        #       - create sheet
        #       - insert header

        # Call the Sheets API
        request = service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=self.sheet_range,
            valueInputOption=value_input_option,
            insertDataOption=insert_data_option,
            body={
                "range": self.sheet_range,
                "majorDimension": "ROWS",
                "values": self._format(reports),
            },
        )

        response = request.execute()
