import rasterio
import os
import numpy as np
import geopandas as gpd
from typing import Any, Dict, List
import pandas as pd
import datetime
import re
from tqdm import tqdm
import rasterio.mask as mask
from geofeather import to_geofeather, from_geofeather
import multiprocessing as mp
from multiprocessing import Pool
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

def parallelize(df,func,n_cores=32):
    df_split=np.array_split(df,n_cores)
    pool=Pool(n_cores)
    df=pd.concat(pool.map(func,df_split))
    pool.close()
    pool.join()
    return df

def join_week_rows(l2):
    df_dummy=pd.DataFrame()
    for i, row in (l2.iterrows()):
	res =map(lambda x: row.append(pd.Series(x,index=['week'])),week_dates)
        df_dummy=df_dummy.append(pd.DataFrame(res), ignore_index=True)
    return df_dummy

def join_var_data(l2):
    df_fin=pd.DataFrame()
    for i, row in (l2.iterrows()):
        geom=[l2['geometry'][i]]
        try :
            tmp_2019, tmp_transform = mask.mask(sen5_2019, geom, crop=True)
            co_mean_2019=np.nanmean(tmp_2019, axis=1)
            co_mean_2019=np.nanmean(co_mean_2019, axis=1)
            df_2020=list(co_mean_2019.reshape(-1,1).T)
            if len(co_mean_2019)==len(week_dates):
		#has to be a unique column in your shape file in this case it is GID_2
                df_new= df_f.loc[df_f['GID_2'] == l2['GID_2'][i]]
                for j in range(0,len(week_2020)):
                    m=(df_new['week']==week_2020[j])
                    df_new.loc[m, 'AOD'] = df_2020[0][j]
                df_fin=df_fin.append(df_new)
        except OSError as err:
            print("OS error: {0}".format(err))      
    return df_fin

if __name__ == "__main__":

        dem=Helper.read_files_ini_dir(PROCESSED_DATA_SOURCE+YEAR)
        var_name=set(dem)
        var_name= [item[19:40] for item in var_name if item.endswith('.tif')]
        week_dates=sorted(var_name)

        vrt_filename=[item for item in var_name if item.contains('.vrt')]
        vrt_file=rasterio.open(os.path.join(vrt_filename))
        level_2=from_geofeather(SHAPE_LEVEL_2)

        df_week_joined=parallelize(level_2,join_week_rows)
	df_final=parallelize(level_2,join_var_data)
        return df_final



