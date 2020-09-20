import os
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import pickle
from tqdm import tqdm
import multiprocessing as mp
from geofeather import to_geofeather, from_geofeather
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

def parallel_initializer(_df_zones):
    global df_zones
    df_zones = _df_zones

def parallel_runner(chunk):
    global df_zones
    return chunk[0], gpd.sjoin(chunk[1], df_zones,how="inner", op = "intersects")

def run(df_zones,df_points,use_parallel, processes):
    np.random.seed(0)

    # Join the data sets
    chunk_count = 20000
    chunks = np.array_split(df_points, chunk_count)
    partial_results = [None] * chunk_count

    if not use_parallel:
        for index, chunk in tqdm(enumerate(chunks), total = chunk_count):
            partial_results[index] = gpd.sjoin(chunk, df_zones, how="inner", op='intersects')

    else:
        with mp.Pool(processes = processes, initializer = parallel_initializer, initargs = (df_zones,)) as pool:
            for index, chunk in tqdm(pool.imap_unordered(parallel_runner, enumerate(chunks)), total = chunk_count):
                partial_results[index] = chunk

    df_join = pd.concat(partial_results)
    return df_join


if __name__ == "__main__":
	with open(PROCESSED_DATA_SOURCES + TEMP+"TEMP_2019.pkl", 'rb') as f:
	    data_TEMP = pickle.load(f)

	crs={'init':'EPSG:4326'}
	geometry = [Point(xy) for xy in zip(data_TEMP['x'], data_TEMP['y'])]
	df_points = gpd.GeoDataFrame(data_TEMP,crs=crs, geometry=geometry)
	df_zones=from_geofeather(PROCESSED_DATA_SOURCES+'Shape_Joined.feather')

	df_joined=run(df_zones,df_points,use_parallel = True, processes = 10)
	
        df_joined=df_joined.reset_index(drop=True)
	aggregations={'NAME_0':'first','value':'mean','TYPE_1':'first','ENGTYPE_1':'first','GID_0':'first','GID_1':'first'}
	temp_grouped=df_joined.groupby(['date_range','NAME_1']).agg(aggregations)
        temp_grouped.to_csv(PROCESSED_DATA_SOURCES+'temp_19.csv')


