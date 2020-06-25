from .base import BaseGoogleService


class GoogleDriveService(BaseGoogleService):
    token_name = 'drive.token.pickle'
    scopes = ['https://www.googleapis.com/auth/drive']

    def __init__(self, encoded_sa_key):
        super(GoogleDriveService, self).__init__(encoded_sa_key, 'drive', 'v3')

    def list_files(self, parents=None):
        page_token = None
        files = []
        query = ""
        if parents:
            query = "'{}' in parents".format(parents[0])
        while True:
            # Call the Drive v3 API
            results = self.service.files().list(
                q=query, pageSize=10, pageToken=page_token,
                fields="nextPageToken, files(id, name)").execute()
            files += results.get('files', [])
            page_token = results.get('nextPageToken')
            if not page_token:
                return files

    def get_file_by_name(self, name, parents=None):
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
