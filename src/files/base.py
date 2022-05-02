from typing import Protocol
import pandas as pd


class IFileExtension(Protocol):

    def read(self, file_path: str) -> pd.DataFrame:
        ...

