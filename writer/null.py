from .base import BaseWriter


class NullWriter(BaseWriter):
    def write(self, reports):
        # do nothing
        pass
