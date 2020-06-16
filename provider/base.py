from abc import ABCMeta, abstractmethod


class BaseProvider(metaclass=ABCMeta):
    def __init__(self, config={}):
        self.config = config

    @abstractmethod
    def fetch(self):
        return BaseResponse()


class BaseResponse(metaclass=ABCMeta):
    def __enter__(self):
        return self

    @abstractmethod
    def to_dict(self):
        return {}

    def close(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
