#!/usr/bin/env python3
from abc import ABC, abstractmethod


class ISpreadsheet(ABC):
    @abstractmethod
    def get_average(self, tab: str='Sheet1') -> float:
        pass

    @abstractmethod
    def get_stdev(self, tab: str='Sheet1') -> float:
        pass
