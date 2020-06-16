from .base import BaseReport


class AdReport(BaseReport):
    def __init__(self, date='', time='', name='', impression=0,
                 click=0, conversion=0, used_budget=0):
        super(AdReport, self).__init__()
        self.name = name
        self.date = date
        self.time = time
        self.impression = impression
        self.click = click
        self.conversion = conversion
        self.used_budget = used_budget

    def _calc_ctr(self):
        if self.click > 0 and self.impression > 0:
            return self.click / self.impression
        else:
            return 0.0

    def _calc_cvr(self):
        if self.conversion > 0 and self.click > 0:
            return self.conversion / self.click
        else:
            return 0.0

    def _calc_cpc(self):
        if self.used_budget > 0 and self.click > 0:
            return self.used_budget / self.click
        else:
            return 0.0

    def _calc_cpm(self):
        if self.used_budget > 0 and self.impression > 0:
            return self.used_budget / self.impression * 1000
        else:
            return 0.0

    def to_dict(self):
        return {
            'provider': self.name,
            'date': self.date,
            'time': self.time,
            'impression': self.impression,
            'click': self.click,
            'conversion': self.conversion,
            'used_budget': self.used_budget,
            'ctr': self._calc_ctr(),
            'cvr': self._calc_cvr(),
            'cpc': self._calc_cpc(),
            'cpm': self._calc_cpm(),
        }
