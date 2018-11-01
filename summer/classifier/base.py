from abc import ABC, abstractmethod

from buttworld.logger import get_logger


class BaseClassifier(ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__.lower())

    @abstractmethod
    def classify(self, *args, **kwargs):
        pass

    def save(self):
        pass

    @abstractmethod
    def load(self, filename: str):
        pass

    @property
    def name(self):
        return self.__class__.__name__
