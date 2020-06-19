from .base import BaseProvider, BaseResponse
from report import AdReport

import google.ads.google_ads.client

class GoogleAds(BaseProvider):
    def __init__(self, config=None):
        super(GoogleAds, self).__init__(config=config)

    def fetch(self):

        credentials = {
            'developer_token': self.config['DEVELOPER_TOKEN'],
            'refresh_token': self.config['REFRESH_TOKEN'],
            'client_id': self.config['CLIENT_ID'],
            'client_secret': self.config['CLIENT_SECRET'],
            'login_customer_id': self.config['MCC_CUSTOMER_ID'],
            }
        
        client = google.ads.google_ads.client.GoogleAdsClient.load_from_dict(credentials)

        customer_id = self.config['CLIENT_CUSTOMER_ID']
        ga_service = client.get_service('GoogleAdsService', version='v3')

        query = (
                'SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks , metrics.conversions '
                'FROM campaign'
                )

        response = ga_service.search_stream(customer_id, query) 

        ret_data=[]

        try:
            for batch in response:
                for row in batch.results:
                    campaign = row.campaign
                    metrics = row.metrics

                    ret_data += [{
                                'campaign': campaign.name.value,
                                'date':'YYYY/MM/DD',
                                'impression': metrics.impressions.value,
                                'click': metrics.clicks.value,
                                'conversion': metrics.all_conversions_value.value,
                                'used_budget': 0,
                                }]
            ret_state='ok'

        except google.ads.google_ads.errors.GoogleAdsException as ex:
            print('Request with ID "%s" failed with status "%s" and includes the '
                    'following errors:' % (ex.request_id, ex.error.code().name))
            for error in ex.failure.errors:
                print('\tError with message "%s".' % error.message)
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print('\t\tOn field: %s' % field_path_element.field_name)
            ret_data += [{
                        'campaign': '---',
                        'date': '0000/00/00',
                        'impression': -1,
                        'click': -1,
                        'conversion': -1,
                        'used_budget': -1,
                        }]
            ret_state='ng'

        return GoogleAdsResponse(ret_state, ret_data)

    def build_reports(self, data, **kwargs):
        ret_data = []
        for row in data:
            ret_data += [
                        AdReport(
                            date=row['date'],
                            time=kwargs['time'],
                            name='google '+row['campaign'],
                            impression=row['impression'],
                            click=row['click'],
                            conversion=row['conversion'],
                            used_budget=row['used_budget'],
                            )
                        ]

        return ret_data


class GoogleAdsResponse(BaseResponse):
    def __init__(self, status, data):
        super(GoogleAdsResponse, self).__init__(status, data)
