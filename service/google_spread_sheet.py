from .base import BaseGoogleService


class GoogleSpreadSheetService(BaseGoogleService):
    token_name = 'sheets.token.pickle'
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, credentials_path):
        super(GoogleSpreadSheetService, self).__init__(credentials_path, 'sheets', 'v4')

    def add_sheet(self, spreadsheet_id, name):
        return self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': name,
                        }
                    }
                }]
            }
        ).execute()

    def list_sheets(self, spreadsheet_id):
        meta = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        return meta.get('sheets', '')

    def get_sheet_by_name(self, spreadsheet_id, name):
        sheets = self.list_sheets(spreadsheet_id)
        for sheet in sheets:
            if sheet['properties']['title'] == name:
                return sheet
        return None

    def insert_rows(self, spreadsheet_id, sheet_range, value_input_option, insert_data_option,
                    rows):
        request = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption=value_input_option,
            insertDataOption=insert_data_option,
            body={
                "range": sheet_range,
                "majorDimension": "ROWS",
                "values": rows,
            },
        )
        return request.execute()
