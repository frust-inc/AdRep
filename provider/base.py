from abc import ABCMeta, abstractmethod


class BaseProvider(metaclass=ABCMeta):
    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def fetch(self):
        return

    @abstractmethod
    def build_reports(self):
        return []

class BaseResponse(metaclass=ABCMeta):
    def __init__(self, status, data):
        self._status = status
        self._data = data

    @property
    def status(self):
        return self._status

    @property
    def data(self):
        return self._data

    def __enter__(self):
        return self

    def close(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
