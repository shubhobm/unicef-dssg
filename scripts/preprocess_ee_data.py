import pandas as pd
import bootstrap  # noqa
from unicef_dssg.lib.helper import Helper
from unicef_dssg.config import (
    PROCESSED_DATA_SOURCES,
    CONCATENATED_DATA_SOURCES,
    AOD,
    NO2,
    TEMP,
    LAND_USE,
    PRECIP,
    POP_DEN,
)
from joblib import Parallel, delayed
from tqdm import tqdm


class PreprocessEEData:
    def execute(
        self,
        df_list,
    ):
        df = self.creating_datetime_column(self._concat_year_df(df_list))
        df.to_pickle(f"{CONCATENATED_DATA_SOURCES}NO2.pkl")

    def creating_datetime_column(self, df):
        df["date"] = [x[0:10] for x in df["date_range"]]
        df["date"] = pd.to_datetime(df["date"])
        return df

    def _concat_year_df(self, df_list):
        return pd.concat(df_list).reset_index(drop=True)


if __name__ == "__main__":
    variable_pkl = Helper.read_files_in_dir(PROCESSED_DATA_SOURCES + TEMP)
    variable_set = set(variable_pkl)
    Parallel(n_jobs=-1, prefer="threads", verbose=5)(
        delayed(PreprocessEEData().execute)(
            list(
                pd.read_pickle(f"{PROCESSED_DATA_SOURCES}{TEMP}{variable_name}"),
                pd.read_pickle(f"{PROCESSED_DATA_SOURCES}{TEMP}{variable_name}"),
            )
        )
        for variable_name in tqdm(variable_set)
    )