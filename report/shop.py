from .base import BaseReport


class ShopReport(BaseReport):
    def __init__(self, date='', time='', name='', regular_sales_num=0,
                 subs_sales_num=0, regular_sales=0, subs_sales=0):
        super(ShopReport, self).__init__()
        self.name = name
        self.date = date
        self.time = time
        self.regular_sales_num = regular_sales_num
        self.subs_sales_num = subs_sales_num
        self.regular_sales = regular_sales
        self.subs_sales = subs_sales

    def _calc_sales_num_sum(self):
        return self.regular_sales_num + self.subs_sales_num

    def _calc_sales_sum(self):
        return self.regular_sales + self.subs_sales

    def to_dict(self):
        return {
            'provider': self.name,
            'date': self.date,
            'time': self.time,
            'regular_sales_num': self.regular_sales_num,
            'subs_sales_num': self.subs_sales_num,
            'sales_num_sum': self._calc_sales_num_sum(),
            'regular_sales': self.regular_sales,
            'subs_sales': self.subs_sales,
            'sales_sum': self._calc_sales_sum(),
        }
