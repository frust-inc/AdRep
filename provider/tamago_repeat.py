from .base import BaseProvider, BaseResponse
from report import ShopReport


class TamagoRepeat(BaseProvider):
    def __init__(self, config=None):
        super(TamagoRepeat, self).__init__(config=config)

    def fetch(self):
        return TamagoRepeatResponse('ok', {
            'date': '2020/06/01',
            'regular_sales_num': 100,
            'subs_sales_num': 80,
            'regular_sales': 300000,
            'subs_sales': 240000,
        })

    def build_reports(self, data, **kwargs):
        return [
            ShopReport(
                name='たまごリピート',
                date=data['date'],
                time=kwargs['time'],
                regular_sales_num=data['regular_sales_num'],
                subs_sales_num=data['subs_sales_num'],
                regular_sales=data['regular_sales'],
                subs_sales=data['subs_sales'],
            )
        ]


class TamagoRepeatResponse(BaseResponse):
    def __init__(self, status, data):
        super(TamagoRepeatResponse, self).__init__(status, data)
