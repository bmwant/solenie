from abc import ABC, abstractmethod

from buttworld.logger import get_logger


class BaseFeatureFinder(ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__.lower())

    @abstractmethod
    def save(self, filename):
        """
        Saves featureset
        """

    @abstractmethod
    def load(self, filename):
        """
        Loads featureset from a file.
        """
