import pandas as pd


class CsvParser:

    @staticmethod
    def read(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)


class ParquetParser:

    @staticmethod
    def read(file_path: str) -> pd.DataFrame:
        return pd.read_parquet(file_path)
