from abc import ABC, abstractmethod

from buttworld.logger import get_logger


class BaseReviewGenerator(ABC):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__.lower())

    @abstractmethod
    def initialize_model(self, *args, **kwargs):
        pass

    @abstractmethod
    def create_good_review(self, length: int):
        pass

    @abstractmethod
    def create_bad_review(self, length: int):
        pass

    @abstractmethod
    def create_neutral_review(self, length: int):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}'
