from abc import ABCMeta, abstractmethod


class BaseProvider(metaclass=ABCMeta):
    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def fetch(self):
        return


class BaseResponse(metaclass=ABCMeta):
    def __enter__(self):
        return self

    @abstractmethod
    def to_dict(self):
        return {}

    def close(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class BaseAdResponse(BaseResponse):
    name = ''

    def __init__(self, date, impression, click, conversion, used_budget):
        super(BaseAdResponse, self).__init__()
        self.date = date
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
            'provider': self.__class__.name,
            'date': self.date,
            'impression': self.impression,
            'click': self.click,
            'conversion': self.conversion,
            'used_budget': self.used_budget,
            'ctr': self._calc_ctr(),
            'cvr': self._calc_cvr(),
            'cpc': self._calc_cpc(),
            'cpm': self._calc_cpm(),
        }
