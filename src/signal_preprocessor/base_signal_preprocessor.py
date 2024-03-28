from abc import ABC, abstractmethod


class BaseSignalPreprocessor(ABC):

    @abstractmethod
    def save_to_file(self, file_path):
        pass

    @abstractmethod
    def read_from_file(self, file_path):
        pass

    @abstractmethod
    def run(self):
        pass