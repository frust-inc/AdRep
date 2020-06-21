from service import BaseService


class DummyGoogleSpreadSheetService(BaseService):
    def __init__(self, credentials_path):
        self.calls = []

I   def add_sheet(self, spreadsheet_id, name):
        self.calls.append('add_sheet')

    def delete_sheet(self, spreadsheet_id):
        self.calls.append('delete_sheet')
