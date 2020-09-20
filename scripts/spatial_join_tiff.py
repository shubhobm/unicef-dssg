import bootstrap  # noqa
from joblib import Parallel, delayed
import pandas as pd
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from unicef_dssg.config import (
    SECONDARY_DATA_SOURCES,
    PROCESSED_DATA_SOURCES,
    YEAR_2019,
    YEAR_2020,
    AOD,
    NO2,
    CITY_ALL,
    LAND_USE,
    PRECIP,
    POP_DEN,
    SATELLITE_DATA,
)
from unicef_dssg.lib.helper import Helper
from tqdm import tqdm


class SpatialJoinTiff:
    def __init__(self, waqi_data: pd.DataFrame):
        self.waqi_data = waqi_data

    def execute(self, AOD_data):
        AOD_geom = self._load_raster(AOD_data)
        AOM_gdf = self._raster_to_gdf(AOD_geom)
        # data_pd_concat.to_pickle(f"{PROCESSED_DATA_SOURCES}{AOD}AOD_2019.pkl")

    def _load_raster(self, AOD_data):
        with rasterio.open(AOD_data) as dataset:
            # Read the dataset's valid data mask as a ndarray.
            mask = dataset.dataset_mask()
            # Extract feature shapes and values from the array.
            for geom, val in rasterio.features.shapes(mask, transform=dataset.transform):
                # Transform shapes from the dataset's own coordinate
                # reference system to CRS84 (EPSG:4326).
                geom = rasterio.warp.transform_geom(dataset.crs, "EPSG:4326", geom, precision=6)
                # Print GeoJSON shapes to stdout.
        print(geom)
        return geom

    def _raster_to_gdf(self, AOD_geom) -> gpd.GeoDataFrame:
        AOD_geom_list = list(AOD_geom)
        print(AOD_geom_list)
        AOD_gdf = gpd.GeoDataFrame.from_features(AOD_geom_list)
        print(AOD_gdf)

    # def create_df_with_datetime(self, variable_name):
    #     search_group = re.search("7_(.*).tif", variable_name)
    #     date = search_group.group(1)
    #     data = gs.from_file(f"{SECONDARY_DATA_SOURCES}{YEAR_2019}{AOD}{variable_name}")
    #     data_pd = data.to_pandas()
    #     data_pd["date_range"] = date
    #     return data_pd


if __name__ == "__main__":
    spatial_join_tiff = SpatialJoinTiff(
        pd.read_csv(f"{PROCESSED_DATA_SOURCES}{CITY_ALL}waqi_data_2019_2020_no_extra_cols.csv"),
    )

    variable_pkl = Helper.read_files_in_dir(
        f"{SECONDARY_DATA_SOURCES}{SATELLITE_DATA}{AOD}{YEAR_2019}"
    )
    variable_set = set(variable_pkl)
    Parallel(n_jobs=-1, prefer="threads", verbose=5)(
        delayed(spatial_join_tiff.execute)(
            f"{SECONDARY_DATA_SOURCES}{SATELLITE_DATA}{AOD}{YEAR_2019}{variable_name}",
        )
        for variable_name in tqdm(variable_set)
    )
