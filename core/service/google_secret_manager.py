from google.cloud import secretmanager

from .base import BaseService


class GoogleSecretManager(BaseService):
    def __init__(self, project_id):
        super(GoogleSecretManager, self).__init__()
        self.project_id = project_id

    def build(self):
        return secretmanager.SecretManagerServiceClient()

    def get(self, key, version='latest'):
        name = self.service.secret_version_path(self.project_id, key, version)
        response = self.service.access_secret_version(name)
        return(response.payload.data.decode('UTF-8'))
