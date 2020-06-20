from .base import BaseProvider, BaseResponse
from report import ShopReport


class TamagoRepeat(BaseProvider):
    def __init__(self, config=None):
        super(TamagoRepeat, self).__init__(config=config)

    def fetch(self):
        return TamagoRepeatResponse('ok', {})

    def build_reports(self, data, **kwargs):
        return [
            ShopReport()
        ]


class TamagoRepeatResponse(BaseResponse):
    def __init__(self, status, data):
        super(TamagoRepeatResponse, self).__init__(status, data)
