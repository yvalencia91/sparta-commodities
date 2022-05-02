from scipy import stats
import numpy as np
import pandas as pd
from datetime import datetime
from settings import config
from src.utils.extensions import export_dataframe


class ZScore:

    def run(self, df: pd.DataFrame) -> None:
        df = df[(np.abs(stats.zscore(df)) < 4).all(axis=1)]
        fig = df.plot(figsize=(20, 10)).get_figure()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        export_dataframe(df, f"{config.file['output']['path']}/data", timestamp, config.file['output']['extension'])
        fig.savefig(f"{config.file['output']['path']}/img/df_{timestamp}")
