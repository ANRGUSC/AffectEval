from abc import ABC, abstractmethod


class BaseFeatureSelector(ABC):

    @abstractmethod
    def run(self):
        pass