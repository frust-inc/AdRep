from abc import ABCMeta, abstractmethod


class BaseReport(metaclass=ABCMeta):

    @abstractmethod
    def to_dict(self):
        return
