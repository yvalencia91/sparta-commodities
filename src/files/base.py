from typing import Protocol
import pandas as pd


class IFileExtension(Protocol):

    def __call__(self, file_path: str) -> pd.DataFrame:
        ...

