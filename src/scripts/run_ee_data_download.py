import bootstrap  # noqa
import ee
from lib.download_ee_data import ImportEarthEngineData


class run_data_import:
    ee.Initialize()

    import_earth_engine_data = ImportEarthEngineData()
    dates = import_earth_engine_data.create_import_params()
    for i in range(len(dates) - 1):
        task = import_earth_engine_data.start_ee_data_download_process(i, dates)


if __name__ == "__main__":
    run_data_import()
