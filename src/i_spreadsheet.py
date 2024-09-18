#!/usr/bin/env python3
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd


class ISpreadsheet(ABC):
    @abstractmethod
    def get_num_observations(self, tab_name: str = "Sheet1") -> np.ndarray:
        pass

    @abstractmethod
    def get_dataframe(self, tab_name: str = "Sheet1") -> pd.DataFrame:
        pass

    @abstractmethod
    def _get_averages(self, tab_name: str = "Sheet1") -> float:
        pass

    @abstractmethod
    def _get_stdevs(self, tab: str = "Sheet1") -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
