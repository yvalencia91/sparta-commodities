import pandas as pd


class CsvParser:

    def __call__(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)


class ParquetParser:

    def __call__(self, file_path: str) -> pd.DataFrame:
        return pd.read_parquet(file_path)
