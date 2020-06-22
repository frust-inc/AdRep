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
                'SELECT metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros '
                'FROM customer'
                )

        response = ga_service.search_stream(customer_id, query) 

        try:
            for batch in response:
                for row in batch.results:
                    metrics = row.metrics

                    ret_data = {
                                'date':'YYYY/MM/DD',
                                'impression': metrics.impressions.value,
                                'click': metrics.clicks.value,
                                'conversion': metrics.all_conversions_value.value,
                                'used_budget': metrics.cost_micros.value,
                                }
            ret_state='ok'

        except google.ads.google_ads.errors.GoogleAdsException as ex:
            print('Request with ID "%s" failed with status "%s" and includes the '
                    'following errors:' % (ex.request_id, ex.error.code().name))
            for error in ex.failure.errors:
                print('\tError with message "%s".' % error.message)
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print('\t\tOn field: %s' % field_path_element.field_name)
            ret_data += {
                        'date': '0000/00/00',
                        'impression': -1,
                        'click': -1,
                        'conversion': -1,
                        'used_budget': -1,
                        }
            ret_state='ng'

        return GoogleAdsResponse(ret_state, ret_data)

    def build_reports(self, data, **kwargs):
    
        ret_data = [
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

        return ret_data


class GoogleAdsResponse(BaseResponse):
    def __init__(self, status, data):
        super(GoogleAdsResponse, self).__init__(status, data)
