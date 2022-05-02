from logging import getLogger
from settings import config, file_extension_factory
from src.libs.logger import setup_logger
from src.utils.errors import FileValidationError, MissingMandatoryColumns
from src.utils.validator import SolverFormatProblem
from src.outliers.base import OutlierStrategy
from src.outliers.strategy import ZScore

setup_logger(config)
log = getLogger(__name__)


def main():
    s = SolverFormatProblem(config=config)

    try:
        is_supported = s.supported_extension()

        if is_supported:
            full_path = f"{s.file_path}/{s.file_name}"
            file_parser = file_extension_factory(file_suffix=s.file_suffix)
            s.df = file_parser.read(file_path=full_path)
            s.raw_data_structure = s.df.dtypes.apply(lambda x: x.name).to_dict()

            v1 = s.check_for_mandatory_columns()
            v2 = s.check_for_datetime_iso8601()
            v3 = s.check_for_rbob_only()
            v4 = s.check_for_month_year_structure()
            v5 = s.check_for_delivery_price()
            v6 = s.check_for_null_values()

            if v1 and v2 and v3 and v4 and v5 and v6:
                log.info("Dataframe is ready to be processed")
                df_pivot = s.df.pivot_table("dlvd_price", "generated_on", "load_month")

                log.info(f"Removing outliers using {config.file['data']['outliers'][0]} strategy")

                clean_data = OutlierStrategy(ZScore())
                clean_data.strategy.run(df_pivot)

                log.info("Outlier removed correctly an image has been produced.")
            else:
                log.warning("One of the validators return False")

    except FileValidationError:
        log.error(f"File path: {s.file_path}")
        log.error(f"Currently we are not supporting this type of file: {s.file_suffix}")

    except MissingMandatoryColumns as m:
        log.error(m)

    except ValueError as v:
        log.error(v)


if __name__ == '__main__':
    main()
