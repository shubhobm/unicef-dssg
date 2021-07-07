import datetime
import ee
from config import ParamsConfig


class ImportEarthEngineData:
  def create_import_params(self):
    start = datetime.date(ParamsConfig.year,ParamsConfig.mon_start,ParamsConfig.date_start)
    end = datetime.date(ParamsConfig.year,ParamsConfig.mon_end,ParamsConfig.date_end)
    dateList = self._date_range(start, end)
    dates =[str(date) for date in dateList]

    return dates

  def start_ee_data_download_process(self, dates, i):
    s_date=dates[i]
    e_date=dates[i+1]
    area = ee.Geometry.Rectangle([ParamsConfig.minx, ParamsConfig.maxy, ParamsConfig.maxx, ParamsConfig.miny])
    collection = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2').select('NO2_column_number_density').filterDate(s_date, e_date);

    img=collection.mean()

    down_args = {
    'image': img,
    'folder': 'src/lib/data/air_pollution',
    'description': 'sentinel5_'+'NO2_column_number_density'+'_'+s_date+'_'+e_date,
    'scale': 7000
    }
    task = ee.batch.Export.image.toDrive(**down_args)
    return task.start()

  def _date_range(self,start, end):
    r = (end+datetime.timedelta(days=1)-start).days
    return [start+datetime.timedelta(days=i) for i in range(0,r,7)]
