#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np


class ISpreadsheet(ABC):
    @abstractmethod
    def get_num_observations(self, tab_name: str='Sheet1') -> np.ndarray:
        pass

    @abstractmethod
    def get_average_of_averages(self, tab_name: str='Sheet1') -> Tuple[float, float]:
        pass

    @abstractmethod
    def __get_averages(self, tab: str= 'Sheet1') -> float:
        pass

    @abstractmethod
    def __get_stdevs(self, tab: str= 'Sheet1') -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass