from .base import BaseWriter


class StdOutWriter(BaseWriter):
    def write(self, values):
        print(values)
