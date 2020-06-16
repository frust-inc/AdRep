from abc import ABCMeta, abstractmethod


class BaseWriter(metaclass=ABCMeta):
    def __init__(self, config={}):
        self.config = config

    def __enter__(self):
        return self

    @abstractmethod
    def write(self, values):
        return

    def close(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
