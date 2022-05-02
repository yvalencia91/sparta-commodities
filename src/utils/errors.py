from builtins import Exception
from typing import List


class FileValidationError(Exception):
    def __str__(self):
        return "Couldn't find a valid extension. Please check whether we support this file extension."


class MissingMandatoryColumns(Exception):
    def __init__(self, cols: List):
        self.cols = ", ".join(cols)

    def __str__(self):
        return f"The following columns are missing: {self.cols}"


class DatetimeParsingFailed(Exception):
    def __init__(self, msg: ValueError):
        self.msg = msg

    def __str__(self):
        return f"Dateformat couldn't be autoparse by pandas to_datetime: {self.msg}"
