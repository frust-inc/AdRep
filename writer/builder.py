from .csv import CSVWriter
from .null import NullWriter
from .stdout import StdOutWriter
from .google_spread_sheet import GoogleSpreadSheetWriter


class WriterBuilder():
    def __init__(self, config=None):
        self.config = config

    def build(self):
        if self.config["TYPE"] == "STDOUT":
            return StdOutWriter(config=self.config)
        if self.config["TYPE"] == "NULL":
            return NullWriter(config=self.config)
        if self.config["TYPE"] == "CSV":
            return CSVWriter(config=self.config)
        if self.config["TYPE"] == "GOOGLE_SPREAD_SHEET":
            return GoogleSpreadSheetWriter(config=self.config)
        raise ValueError("invalid TYPE is specified.")
