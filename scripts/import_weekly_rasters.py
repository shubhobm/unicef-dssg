import bootstrap  # noqa
from joblib import Parallel, delayed
import pandas as pd
import georasters as gs
import re
from unicef_dssg.config import (
    SECONDARY_DATA_SOURCES,
    PROCESSED_DATA_SOURCES,
    YEAR_2019,
    YEAR_2020,
    AOD,
    NO2,
    LAND_USE,
    PRECIP,
    POP_DEN,
)
from unicef_dssg.lib.helper import Helper
from tqdm import tqdm


class ImportWeeklyRasters:
    def execute(self, variable_name):
        data_pd_concat = self.concatenate_geotiff_to_dataframe(variable_name)
        data_pd_concat.to_pickle(f"{PROCESSED_DATA_SOURCES}{PRECIP}precip__2019.pkl")

    def concatenate_geotiff_to_dataframe(self, variable_name):
        file_list = []
        search_group = re.search("__(.*).tif", variable_name)
        date = search_group.group(1)
        data = gs.from_file(f"{SECONDARY_DATA_SOURCES}{YEAR_2019}{PRECIP}{variable_name}")
        data_pd = data.to_pandas()
        data_pd["date_range"] = date
        file_list.append(data_pd)
        data_pd_concat = pd.concat(file_list).reset_index(drop=True)
        return data_pd_concat


if __name__ == "__main__":
    variable_pkl = Helper.read_files_in_dir(SECONDARY_DATA_SOURCES + YEAR_2019 + PRECIP)
    variable_set = set(variable_pkl)
    Parallel(n_jobs=-1, prefer="threads", verbose=5)(
        delayed(ImportWeeklyRasters().execute)(variable_name)
        for variable_name in tqdm(variable_set)
    )
