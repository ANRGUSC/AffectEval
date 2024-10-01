from abc import ABC, abstractmethod


class BaseLabelGenerator(ABC):

    @abstractmethod
    def run(self):
        pass
