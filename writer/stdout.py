from .base import BaseWriter


class StdOutWriter(BaseWriter):
    def write(self, reports):
        for report in reports:
            print(report.to_dict())
