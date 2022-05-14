from logging import getLogger
from typing import Dict

from settings import config, ColumnPosition
from src.libs.logger import setup_logger
from src.utils.errors import FileValidationError, MissingMandatoryColumns
from src.utils.validator import SolverFormatProblem
from src.outliers.base import OutlierStrategy
from src.outliers.strategy import ZScore

setup_logger(config)
log = getLogger(__name__)


def main(params: Dict):

    try:
        solver = SolverFormatProblem(**params)
        df_pivot = solver.df.pivot_table(solver.pos.y_axis['column'], solver.pos.x_axis['column'], solver.pos.label['column'])

        log.info(f"Removing outliers using {config.file['data']['outliers'][0]} strategy")

        clean_data = OutlierStrategy()
        clean_data(strategy=ZScore(), df=df_pivot)

        log.info("Outlier removed correctly an image has been produced.")

    except FileValidationError:
        log.error(f"Currently we are not supporting this type of file")

    except MissingMandatoryColumns as m:
        log.error(m)

    except ValueError as v:
        log.error(v)


if __name__ == '__main__':

    values = {
        "full_path": f"{config.file['path']}/{config.file['name']}",
        "output_path": config.file['output']['path'],
        "extensions": config.file['supported']

    }

    main(params=values)

