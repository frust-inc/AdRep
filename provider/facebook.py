from .base import BaseProvider, BaseResponse
from report import AdReport
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights


class Facebook(BaseProvider):
    def __init__(self, config=None):
        super(Facebook, self).__init__(config=config)

    def fetch(self, target_date):
        # init FacebookAdsApi
        FacebookAdsApi.init(
                self.config['APP_ID'],
                self.config['APP_SECRET'],
                self.config['ACCESS_TOKEN']
                )
        my_account = AdAccount('act_'+self.config['AD_ACCOUNT_ID'])

        fields = [AdsInsights.Field.impressions,
                  AdsInsights.Field.clicks,
                  AdsInsights.Field.conversions,
                  ]

        target_date_str = target_date.strftime('%Y-%m-%d')
        params = {
                'time_range': {
                    'since': target_date_str,
                    'until': target_date_str,
                    },
                }

        # data fetch
        response = my_account.get_insights(fields=fields, params=params)

        # dummy response for develop
        dummy_response = {
                "data": [
                    {
                        "impressions": "200",
                        "clicks": "60",
                        "conversions": "20",
                        "date_start": "2009-03-28",
                        "date_stop": "2016-04-01",
                    },
                    {
                        "impressions": "300",
                        "clicks": "90",
                        "conversions": "30",
                        "date-start": "2009-03-28",
                        "date_stop": "2016-04-01",
                    },
                    ],
                "paging": {
                    "cursors": {
                        "before": "MAZDZD",
                        "after": "MAZDZD",
                        }
                    }
                }

        ret = []
        for row in dummy_response['data']:
            ret.append({
                'date': row['date_stop'],
                'format': 'format',
                'impression': int(row['impressions']),
                'click': int(row['clicks']),
                'conversion': int(row['conversions']),
                'used_budget': int('10'),
                })

        return FacebookResponse('ok', ret)

    def build_reports(self, data, **kwargs):

        ret = []
        for row in data:
            ret.append(
                    AdReport(
                        date=row['date'],
                        time=kwargs['time'],
                        name='facebook',
                        format_='format',
                        impression=row['impression'],
                        click=row['click'],
                        conversion=row['conversion'],
                        used_budget=row['used_budget'],
                        )
                    )

        return ret


class FacebookResponse(BaseResponse):
    def __init__(self, status, data):
        super(FacebookResponse, self).__init__(status, data)
