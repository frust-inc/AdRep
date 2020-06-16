from .base import BaseProvider, BaseAdResponse


class GoogleAdSense(BaseProvider):
    def __init__(self, config=None):
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


class GoogleAdSenseResponse(BaseAdResponse):
    name = 'google'
