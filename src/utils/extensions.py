import pandas as pd


def export_dataframe(df: pd.DataFrame, path: str, timestamp: str, extension: str) -> None:
    convert_to = {
        "parquet": df.to_parquet,
        "csv": df.to_csv
    }

    convert_to[extension](f"{path}/df_{timestamp}.{extension}")
