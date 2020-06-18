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
            'client_secret': self.config['CLIENT_SECRET']
            }
        
        client = google.ads.google_ads.client.GoogleAdsClient.load_from_dict(credentials)

        ### debug ###
        page_size = 1000
        customer = "8442677458"
        ga_service = client.get_service('GoogleAdsService', version='v1')

        query = (
                'SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks, metrics.all_conversions_value'
                'FROM campaign'
                )

        response = ga_service.search(customer, query, page_size=page_size)

        try:
            for row in response:
                campaign = row.campaign
                metrics = row.metrics

                print('CAMPAIGN_ID: %d'
                      'CAMPAIGN_NAME: %s'
                      'IMPRESSIONS: %d'
                      'CLICKS: %d'
                      'CONVERSIONS: %d'
                    % (campaign.id.value, campaign.name.value,
                       metrics.impressions.value, metrics.clicks.value, 
                       metrics.all_conversions_value.value))

        except google.ads.google_ads.errors.GoogleAdsException as ex:
            print('Request with ID "%s" failed with status "%s" and includes the '
                    'following errors:' % (ex.request_id, ex.error.code().name))
            for error in ex.failure.errors:
                print('\tError with message "%s".' % error.message)
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print('\t\tOn field: %s' % field_path_element.field_name)





        #end_debug#

        # Dummy
        # TODO: Fetch from actual data provider
        return GoogleAdsResponse('ok', {
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


class GoogleAdsResponse(BaseResponse):
    def __init__(self, status, data):
        super(GoogleAdsResponse, self).__init__(status, data)
