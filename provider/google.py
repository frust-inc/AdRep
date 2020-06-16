from .base import BaseProvider, BaseResponse


class GoogleAdSense(BaseProvider):
    def __init__(self, config={}):
        super(GoogleAdSense, self).__init__(config=config)

    def fetch(self):
        # TODO: Fetch from actual data provider
        # Dummy
        return GoogleAdSenseResponse(
            '2020/06/01',
            100000,
            1000,
            10,
            30000,
        )


class GoogleAdSenseResponse(BaseResponse):
    name = 'google'

    def __init__(self, date, impression, click, conversion, used_budget):
        super(GoogleAdSenseResponse, self).__init__()
        self.date = date
        self.impression = impression
        self.click = click
        self.conversion = conversion
        self.used_budget = used_budget

    def to_dict(self):
        return {
            'provider': GoogleAdSenseResponse.name,
            'date': self.date,
            'impression': self.impression,
            'click': self.click,
            'conversion': self.conversion,
            'used_budget': self.used_budget,
        }
