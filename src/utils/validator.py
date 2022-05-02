from pathlib import Path
from logging import getLogger
from typing import List, Dict
import pandas as pd
from settings import Config
from src.utils.errors import FileValidationError, MissingMandatoryColumns, DatetimeParsingFailed
from datetime import datetime
log = getLogger(__name__)


class SolverFormatProblem:

    def __init__(self, config: Config):

        self.no_valid_data = pd.DataFrame([])
        self.df: pd.DataFrame = pd.DataFrame([])
        self.file_path: str = config.file["path"]
        self.file_name: str = config.file["name"]
        self.extensions: List = config.file["supported"]
        self.raw_data_structure: Dict = {}
        self.data_structure: Dict = config.file["data"]["structure"]
        self.is_file: bool = False
        self.file_suffix: str = ""
        self.output_path = config.file["output"]["path"]

    def supported_extension(self) -> bool:

        self.is_file = Path(f"{self.file_path}/{self.file_name}").is_file()
        self.file_suffix = Path(f"{self.file_path}/{self.file_name}").suffix.replace('.', '')

        if self.is_file and self.file_suffix in self.extensions:
            log.info("Supported file extension.")
            log.debug(self.file_name)
            return True

        log.info("Check if the file is actually a file and if we support it.")
        raise FileValidationError

    def check_for_mandatory_columns(self) -> bool:

        try:
            loaded_columns = self.df.columns
            mandatory_columns = self.data_structure.keys()
            result = all(elem in loaded_columns for elem in mandatory_columns)

            if result:
                return True

            missing_cols = list(set(mandatory_columns).difference(loaded_columns))
            raise MissingMandatoryColumns(cols=missing_cols)

        except MissingMandatoryColumns as e:
            log.error(e)

    def check_for_datetime_iso8601(self) -> bool:

        try:
            self.df["generated_on"] = pd.to_datetime(self.df["generated_on"])
            return True
        except ValueError as e:
            raise DatetimeParsingFailed(msg=e)

    def check_for_rbob_only(self) -> bool:

        unique_route = self.df["display_name"].unique()

        if "RBOB" in unique_route and len(unique_route) == 1:
            return True

    def check_for_month_year_structure(self) -> bool:

        valid_dtype = pd.to_datetime(self.df["load_month"], format='%b.%y').dtypes.name

        if valid_dtype == self.data_structure["load_month"]:
            return True

    def check_for_delivery_price(self) -> bool:

        actual_dtype = self.df["dlvd_price"].dtypes.name

        if actual_dtype != self.data_structure["dlvd_price"]:
            self.df["dlvd_price"] = self.df["dlvd_price"].astype(float)

        return True

    def check_for_null_values(self) -> bool:

        self.no_valid_data = self.df[self.df.isnull().any(axis=1)]
        self.df = self.df[self.df.notnull().any(axis=1)]

        if len(self.no_valid_data) > 0:
            log.warning("Some null values were found. Applying strategy...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.no_valid_data.to_csv(f"{self.output_path}/no_valid_data/data_nulls_{timestamp}.csv")

        return True
