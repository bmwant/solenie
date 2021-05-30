import os
import time
import platform
from abc import ABC, abstractmethod


class BaseClient(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_bid(self, symbol):
        pass

    @abstractmethod
    def get_ask(self, symbol):
        pass

    @abstractmethod
    def get_tickers(self, *args, **kwargs):
        pass

    @abstractmethod
    def make_order(self, *args, **kwargs):
        pass