#!/usr/bin/env python3
from abc import ABC, abstractmethod


class ISpreadsheet(ABC):
    @abstractmethod
    def get_averages(self, tab: str='Sheet1') -> float:
        pass

    @abstractmethod
    def get_stdevs(self, tab: str='Sheet1') -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass