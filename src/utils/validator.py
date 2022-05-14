from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from logging import getLogger
from typing import AnyStr, Dict

import pandas as pd

from settings import config, file_extension_factory, ColumnPosition
from src.utils.errors import FileValidationError, MissingMandatoryColumns, DatetimeParsingFailed

log = getLogger(__name__)


@dataclass
class SolverFormatProblem:
    full_path: AnyStr
    output_path: AnyStr
    extensions: list = field(default_factory=list)
    df: pd.DataFrame = field(init=False, default=pd.DataFrame([]))
    pos: ColumnPosition = field(init=False)

    def __post_init__(self):
        self.df = file_extension_factory(file_path=self.full_path)
        self.pos = ColumnPosition(**{col.pop('position'): col for col in config.file['data']['structure']})

    def __call__(self):
        is_file = Path(f"{self.full_path}").is_file()
        file_suffix = Path(f"{self.full_path}").suffix.replace('.', '')

        if is_file and file_suffix in self.extensions:
            log.info("Supported file extension.")
            log.debug(self.full_path)
            return True

        log.info("Check if the file is actually a file and if we support it.")
        raise FileValidationError

    def check_for_mandatory_columns(self) -> bool:
        try:
            loaded_columns = self.df.columns
            mandatory_columns = [self.pos.x_axis['column'], self.pos.y_axis['column'], self.pos.label['column'], self.pos.others['column']]
            result = all(elem in loaded_columns for elem in mandatory_columns)

            if result:
                return True

            missing_cols = list(set(mandatory_columns).difference(loaded_columns))
            raise MissingMandatoryColumns(cols=missing_cols)

        except MissingMandatoryColumns as e:
            log.error(e)

    def check_for_datetime_iso8601(self) -> bool:
        try:
            x_axis = self.pos.x_axis
            self.df[x_axis] = pd.to_datetime(self.df[x_axis])
            return True
        except ValueError as e:
            raise DatetimeParsingFailed(msg=e)

    def check_for_rbob_only(self) -> bool:
        others = (self.pos.others['column'], self.pos.others['value'])
        unique_route = self.df[others[0]].unique()

        if others[1] in unique_route and len(unique_route) == 1:
            return True

    def check_for_month_year_structure(self) -> bool:
        label = (self.pos.label['column'], self.pos.label['type'])

        valid_dtype = pd.to_datetime(self.df[label[0]], format='%b.%y').dtypes.name

        if valid_dtype == label[1]:
            return True

    def check_for_delivery_price(self) -> bool:
        y_axis = (self.pos.y_axis['column'], self.pos.y_axis['type'])

        actual_dtype = self.df[y_axis[0]].dtypes.name

        if actual_dtype != y_axis[1]:
            self.df[y_axis[0]] = self.df[y_axis[0]].astype(float)

        return True

    def check_for_null_values(self) -> bool:
        no_valid_data = self.df[self.df.isnull().any(axis=1)]
        self.df = self.df[self.df.notnull().any(axis=1)]

        if len(no_valid_data) > 0:
            log.warning("Some null values were found. Applying strategy...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            no_valid_data.to_csv(f"{self.output_path}/no_valid_data/data_nulls_{timestamp}.csv")

        return True


