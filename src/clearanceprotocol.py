#!/usr/bin/env python3

from dataclasses import dataclass
import pandas as pd


@dataclass
class ClearanceProtocol:
    protocol_id: int
    name: str
    chip_id_lst: list[int]
    percent_cleared: pd.DataFrame
