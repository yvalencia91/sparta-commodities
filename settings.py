from pathlib import Path

import pandas as pd
from pyaml_env import parse_config
from dataclasses import dataclass
from typing import Dict
from src.files.extensions import CsvParser, ParquetParser
import os


@dataclass
class ColumnPosition:
    x_axis: Dict
    y_axis: Dict
    label: Dict
    others: Dict


@dataclass
class Config:
    file: Dict
    logger: Dict


def setup_config(path: str) -> Config:
    cfg = parse_config(path)
    return Config(**cfg)


def file_extension_factory(file_path: str) -> pd.DataFrame:

    file_suffix = Path(file_path).suffix.replace('.', '')

    factories = {
        "csv": CsvParser(),
        "parquet": ParquetParser()
    }
    return factories[file_suffix](file_path=file_path)


config = setup_config(f'{os.path.dirname(__file__)}/settings.yml')
