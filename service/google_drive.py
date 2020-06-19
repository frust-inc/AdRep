from .base import BaseGoogleService


class GoogleDriveService(BaseGoogleService):
    token_name = 'drive.token.pickle'
    scopes = ['https://www.googleapis.com/auth/drive']

    def __init__(self, credentials_path):
        super(GoogleDriveService, self).__init__(credentials_path, 'drive', 'v3')

    def list_files(self, parents=None):
        query = ""
        if parents:
            query = "'{}' in parents".format(parents[0])
        # Call the Drive v3 API
        results = self.service.files().list(
            q=query, pageSize=10, fields="nextPageToken, files(id, name)").execute()
        # XXX: needs to request items of next page
        return results.get('files', [])

    def get_file(self, name, parents=None):
        files = self.list_files(parents=parents)
        find = []
        for f in files:
            if f['name'] == name:
                find.append(f)
        return find

    def create_spreadsheet(self, name, parents=None):
        body = {
            "name": name,
            "parents": parents,
            "mimeType": "application/vnd.google-apps.spreadsheet"
        }
        # Call the Drive v3 API
        return self.service.files().create(body=body).execute()
