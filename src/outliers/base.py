from dataclasses import dataclass
from typing import Protocol
import pandas as pd


class IOutlierFinder(Protocol):

    def run(self, df: pd.DataFrame) -> None:
        ...


@dataclass
class OutlierStrategy:

    def __call__(self, strategy: IOutlierFinder, df: pd.DataFrame):
        strategy.run(df)
