from pyaml_env import parse_config
from dataclasses import dataclass
from typing import Dict
from src.files.base import IFileExtension
from src.files.extensions import CsvParser, ParquetParser
import os


@dataclass
class Config:
    file: Dict
    logger: Dict


def setup_config(path: str) -> Config:
    cfg = parse_config(path)
    return Config(**cfg)


def file_extension_factory(file_suffix: str) -> IFileExtension:
    factories = {
        "csv": CsvParser(),
        "parquet": ParquetParser()
    }
    return factories[file_suffix]


config = setup_config(f'{os.path.dirname(__file__)}/settings.yml')
