from .base import BaseProvider, BaseResponse
from report import AdReport
from collections import defaultdict
import google.ads.google_ads.client


class GoogleAds(BaseProvider):
    def __init__(self, config=None):
        super(GoogleAds, self).__init__(config=config)

    def fetch(self, target_date):
        # googleads init
        credentials = {
            'developer_token': self.config['DEVELOPER_TOKEN'],
            'refresh_token': self.config['REFRESH_TOKEN'],
            'client_id': self.config['CLIENT_ID'],
            'client_secret': self.config['CLIENT_SECRET'],
            'login_customer_id': self.config['MCC_CUSTOMER_ID'],
            }

        client = google.ads.google_ads.client.GoogleAdsClient.load_from_dict(credentials)
        get_type = client.get_type('AdvertisingChannelTypeEnum').AdvertisingChannelType

        customer_id = self.config['CLIENT_CUSTOMER_ID']
        ga_service = client.get_service('GoogleAdsService', version='v3')

        # query request
        target_date_str = target_date.strftime('%Y-%m-%d')
        query = (
                'SELECT campaign.advertising_channel_type,'
                '       metrics.impressions,'
                '       metrics.clicks,'
                '       metrics.conversions,'
                '       metrics.cost_micros '
                'FROM   campaign '
                'WHERE  segments.date = \'{target_date}\''.format(target_date=target_date_str)
                )

        response = ga_service.search_stream(customer_id, query)

        ret_data = []
        try:
            for batch in response:
                for row in batch.results:
                    metrics = row.metrics
                    campaign = row.campaign

                    ret_data.append({
                                'date': target_date.strftime('%Y/%m/%d'),
                                'format': get_type.Name(campaign.advertising_channel_type),
                                'impression': metrics.impressions.value,
                                'click': metrics.clicks.value,
                                'conversion': metrics.all_conversions_value.value,
                                'used_budget': metrics.cost_micros.value,
                                })
            ret_state = 'ok'

        except google.ads.google_ads.errors.GoogleAdsException as ex:
            print('Request with ID "%s" failed with status "%s" and includes the '
                  'following errors:' % (ex.request_id, ex.error.code().name))
            for error in ex.failure.errors:
                print('\tError with message "%s".' % error.message)
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print('\t\tOn field: %s' % field_path_element.field_name)
            ret_state = 'ng'

        return GoogleAdsResponse(ret_state, ret_data)

    def build_reports(self, data, **kwargs):

        # sum metrics data
        # and holds the date
        ddict = defaultdict(lambda: defaultdict(int))
        for row in data:
            ddict[row['format']]['date'] = row['date']
            ddict[row['format']]['impression'] += row['impression']
            ddict[row['format']]['click'] += row['click']
            ddict[row['format']]['conversion'] += row['conversion']
            ddict[row['format']]['used_budget'] += row['used_budget']

        # creates the report
        ret = []
        for key, value in ddict.items():
            ret.append(
                    AdReport(
                        date=value['date'],
                        time=kwargs['time'],
                        name='google',
                        format_=key,
                        impression=value['impression'],
                        click=value['click'],
                        conversion=value['conversion'],
                        used_budget=value['used_budget'],
                        )
                    )

        return ret


class GoogleAdsResponse(BaseResponse):
    def __init__(self, status, data):
        super(GoogleAdsResponse, self).__init__(status, data)
