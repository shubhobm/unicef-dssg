import csv
import os
import re
import pandas as pd
from tqdm import tqdm
from zipfile import ZipFile
import pathlib
import geopandas as gpd
from unicef_dssg.lib.helper import Helper

def convert_to_df(file_name):
  with ZipFile(file_name, 'r') as zipObj:
     listOfFileNames = zipObj.namelist()
     strip_end = re.search("(.*)_shp.zip",file_name)
     raw_name = strip_end.group(1)
     for fileName in listOfFileNames:
        if "_1" in fileName:
           zipObj.extract(fileName,'temp_shp')
  read_fname= pathlib.Path("temp_shp/"+ raw_name+ "_1.shp") 
  if read_fname.exists(): 
    shp=gpd.read_file(read_fname)
    return shp     

def concat_function(file_zip):
  for variable_name in tqdm(file_zip) :
    print(variable_name)
    shp= convert_to_df(variable_name)
    appended_data.append(shp)

if __name__ == "__main__":
    dem=Helper.read_files_ini_dir(PROCESSED_DATA_SOURCE+SHAPE)
    var_name=set(dem)
    var_name= [item for item in var_name if item.endswith('.zip')]
    appended_data = []
    concat_function(var_name)
    shp_concat = pd.concat(appended_data).reset_index(drop=True)
