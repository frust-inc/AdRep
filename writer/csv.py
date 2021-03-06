import csv
import os

from .base import BaseWriter


class CSVWriter(BaseWriter):
    def __init__(self, config=None):
        super(CSVWriter, self).__init__(config=config)

        if 'PATH' in config:
            self.path = config['PATH']
        else:
            raise ValueError('PATH must be specified in config.')

        if 'FIELDNAMES' in config:
            self.fieldnames = config['FIELDNAMES']
        else:
            raise ValueError('FIELDNAMES must be specified in config.')

        self.mode = 'a'  # default mode is append
        if 'MODE' in config:
            self.mode = config['MODE']

        self.write_header = False  # default not write header
        if 'WRITE_HEADER' in config:
            self.write_header = config['WRITE_HEADER']

    def write(self, reports):
        write_header = self.write_header
        if os.path.exists(self.path):
            write_header = False

        with open(self.path, self.mode) as f:
            w = csv.DictWriter(f, fieldnames=self.fieldnames)
            if write_header:
                w.writeheader()
            for report in reports:
                w.writerow(report.to_dict())
