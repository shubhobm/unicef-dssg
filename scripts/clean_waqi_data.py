import bootstrap  # noqa
from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import datetime as dt
import os
from unicef_dssg.config import (
    SECONDARY_DATA_SOURCES,
    PROCESSED_DATA_SOURCES,
    CITY,
    CITY_ALL,
    CITY_COLS,
)
from unicef_dssg.lib.helper import Helper
from tqdm import tqdm


class CleanWaqiData:
    def execute(self, waqi_data_name: str, waqi_data: pd.DataFrame) -> None:
        # self._remove_metadata_rows(waqi_data)
        waqi_data = self._create_week_beginning_col(waqi_data)
        waqi_data = self._create_weekly_average(waqi_data)
        waqi_data = self._create_seperate_variable_cols(waqi_data)
        waqi_data = self._combine_header_rows(waqi_data)
        waqi_data = self._subset_cols_to_process(waqi_data)
        print(waqi_data.shape)
        if not os.path.isfile(f"{PROCESSED_DATA_SOURCES}/{CITY_ALL}waqi_data_2019_2020.csv"):
            waqi_data.to_csv(
                f"{PROCESSED_DATA_SOURCES}/{CITY_ALL}waqi_data_2019_2020.csv",
                header=CITY_COLS,
                index=False,
            )
        else:  # else it exists so append without writing the header
            waqi_data.to_csv(
                f"{PROCESSED_DATA_SOURCES}/{CITY_ALL}waqi_data_2019_2020.csv",
                mode="a",
                header=False,
            )

    def _subset_cols_to_process(self, waqi_data: pd.DataFrame):
        waqi_data = waqi_data[CITY_COLS]
        return waqi_data

    def _create_weekly_average(self, waqi_data: pd.DataFrame):
        waqi_data = (
            waqi_data.groupby(["Week", "Country", "City", "Specie"])
            .agg({"count": "sum", "min": "min", "max": "max", "median": "mean", "variance": "mean"})
            .round(2)
            .reset_index()
        )
        return waqi_data

    def _create_seperate_variable_cols(self, waqi_data: pd.DataFrame):

        waqi_data = waqi_data.pivot_table(
            index=["Week", "Country", "City"],
            columns="Specie",
            values=["count", "min", "max", "median", "variance"],
            aggfunc="first",
        ).reset_index()

        return waqi_data

    def _combine_header_rows(self, waqi_data: pd.DataFrame):
        waqi_data.columns = (
            waqi_data.columns.map("_".join)
            .str.strip()
            .str.lower()
            .str.replace("-", "_")
            .str.replace(" ", "_")
            .str.rstrip("_")
        )
        return waqi_data

    def _create_week_beginning_col(self, waqi_data: pd.DataFrame):
        waqi_data["Date"] = pd.to_datetime(waqi_data["Date"])
        waqi_data["Week"] = waqi_data["Date"] - waqi_data["Date"].dt.weekday * np.timedelta64(
            1, "D"
        )
        waqi_data = waqi_data.drop(["Date"], axis=1)
        return waqi_data

    def _remove_metadata_rows(self, waqi_data: pd.DataFrame):
        return waqi_data.iloc[4:]


if __name__ == "__main__":

    variable_files = Helper.read_files_in_dir(SECONDARY_DATA_SOURCES + CITY)
    variable_set = set(variable_files)
    print(variable_set)
    Parallel(n_jobs=-1, prefer="threads", verbose=5)(
        delayed(CleanWaqiData().execute)(
            variable_name[:-4],
            pd.read_csv(f"{SECONDARY_DATA_SOURCES}{CITY}{variable_name}", error_bad_lines=False),
        )
        for variable_name in tqdm(variable_set)
    )
