import bootstrap  # noqa
from joblib import Parallel, delayed
import pandas as pd
import geopandas as gpd
from unicef_dssg.config import CONCATENATED_DATA_SOURCES, AOD_CITY, CITY_SHAPE, WAQI
from unicef_dssg.lib.helper import Helper
from tqdm import tqdm


class JoinAodWaqiCityData:
    def __init__(self, waqi_data: pd.DataFrame, city_geom: gpd.GeoDataFrame):
        self.waqi_data = waqi_data
        self.city_geom = city_geom

    def execute(self, AOD_data: pd.DataFrame):
        AOD_city_data = self._merge_city_geom_with_AOD_city_data(AOD_data)
        AOD_city_data = self._create_datetime_column(AOD_city_data)
        # data_pd_concat.to_pickle(f"{PROCESSED_DATA_SOURCES}{AOD}AOD_2019.pkl")

    def _merge_city_geom_with_AOD_city_data(self, AOD_data: pd.DataFrame):
        AOD_with_city_geom = AOD_data.merge(self.city_geom, on="NAME_1")
        return AOD_with_city_geom

    def _create_datetime_column(self, AOD_city_data: pd.DataFrame):
        AOD_city_data["date"] = [x[0:10] for x in AOD_city_data["date_range"]]
        AOD_city_data["date"] = pd.to_datetime(AOD_city_data["date"])
        return AOD_city_data

    def _merge_waqi_data_with_AOD_city_date(self, AOD_city_data: pd.DataFrame):
        AOD_city_waqi_data = AOD_city_data.merge(
            self.waqi_data, left_on=["date", "NAME_1"], right_on=["Week", "City"]
        )
        return AOD_city_waqi_data


if __name__ == "__main__":
    join_aod_waqi_city_data = JoinAodWaqiCityData(
        pd.read_csv(f"{CONCATENATED_DATA_SOURCES}{WAQI}WAQI_CONCAT.csv"),
        gpd.read_file(f"{CONCATENATED_DATA_SOURCES}{CITY_SHAPE}city_aq_data.shp"),
    )

    variable_pkl = Helper.read_files_in_dir(f"{CONCATENATED_DATA_SOURCES}{AOD_CITY}")
    variable_set = set(variable_pkl)
    Parallel(n_jobs=-1, prefer="threads", verbose=5)(
        delayed(join_aod_waqi_city_data.execute)(
            f"{AOD_CITY}{variable_name}",
        )
        for variable_name in tqdm(variable_set)
    )
