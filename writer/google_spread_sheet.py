from datetime import datetime

from .base import BaseWriter
from service import GoogleSpreadSheetService, GoogleDriveService


class GoogleSpreadSheetWriter(BaseWriter):
    def __init__(self, config=None):
        super(GoogleSpreadSheetWriter, self).__init__(config=config)

        if "FOLDER_ID" in config:
            self.folder_id = config["FOLDER_ID"]
        else:
            raise ValueError("FOLDER_ID must be specified.")

        if "SPREADSHEET_NAME" in config:
            now = datetime.now()
            self.spreadsheet_name = now.strftime(config["SPREADSHEET_NAME"])
        else:
            raise ValueError("SPREADSHEET_NAME must be specified.")

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

        if "HEADERS" in config:
            self.headers = config["HEADERS"]
        else:
            raise ValueError("HEADERS must be specified.")

        self.value_input_option = 'USER_ENTERED'
        self.insert_data_option = 'OVERWRITE'

        self.sheet_service = GoogleSpreadSheetService(self.credentials_path)
        self.drive_service = GoogleDriveService(self.credentials_path)

    def _headers(self):
        return [self.headers[key] for key in self.fieldnames]

    def _values(self, reports):
        formatted = []
        for report in reports:
            # TODO: data validation
            values = report.to_dict()
            formatted.append([values[header] for header in self.fieldnames])
        return formatted

    def write(self, reports):
        files = self.drive_service.get_file_by_name(self.spreadsheet_name, parents=[self.folder_id])
        if not files:
            # if spreadsheet does not exist, create it.
            sheet = self.drive_service.create_spreadsheet(self.spreadsheet_name,
                                                          parents=[self.folder_id])
        else:
            sheet = files[0]
        sheet_id = sheet['id']

        if not self.sheet_service.get_sheet_by_name(sheet['id'], self.sheet_name):
            # if sheet does not exist, add it.
            self.sheet_service.add_sheet(sheet['id'], self.sheet_name)
            # insert header
            self.sheet_service.insert_rows(sheet_id, self.sheet_range, self.value_input_option,
                                           self.insert_data_option, [self._headers()])
            # delete default sheet
            self.sheet_service.delete_sheet(sheet_id, 0)

        # insert values
        self.sheet_service.insert_rows(sheet_id, self.sheet_range, self.value_input_option,
                                       self.insert_data_option, self._values(reports))
