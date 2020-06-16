from .base import BaseProvider, BaseResponse
from report import AdReport


class GoogleAdSense(BaseProvider):
    def __init__(self, config=None):
        super(GoogleAdSense, self).__init__(config=config)

    def fetch(self):
        # Dummy
        # TODO: Fetch from actual data provider
        return GoogleAdSenseResponse('ok', {
            'date': '2020/06/01',
            'impression': 100000,
            'click': 1000,
            'conversion': 10,
            'used_budget': 30000,
        })

    def build_reports(self, data, **kwargs):
        return [
            AdReport(
                date=data['date'],
                time=kwargs['time'],
                name='google',
                impression=data['impression'],
                click=data['click'],
                conversion=data['conversion'],
                used_budget=data['used_budget'],
            )
        ]


class GoogleAdSenseResponse(BaseResponse):
    def __init__(self, status, data):
        super(GoogleAdSenseResponse, self).__init__(status, data)
