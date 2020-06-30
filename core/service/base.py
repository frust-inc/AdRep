from abc import ABCMeta, abstractmethod
import base64
import json

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class BaseService(metaclass=ABCMeta):
    def __init__(self):
        self._service = None

    @abstractmethod
    def build(self):
        return

    @property
    def service(self):
        if not self._service:
            service = self.build()
            self._service = service
        return self._service


class BaseGoogleService(BaseService):
    token_name = ''
    scopes = []

    def __init__(self, encoded_service_key, api, version):
        super(BaseGoogleService, self).__init__()
        self.encoded_service_key = encoded_service_key
        self.api = api
        self.version = version

    def build(self):
        service_key_json = base64.decodebytes(self.encoded_service_key.encode())
        service_key = json.loads(service_key_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            service_key,
            self.__class__.scopes,
        )

        return build(self.api, self.version, credentials=creds, cache_discovery=False)

    def get(self):
        return self.service
