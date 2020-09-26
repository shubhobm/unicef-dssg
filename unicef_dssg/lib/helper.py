import csv
import os
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd


class Helper:
    @staticmethod
    def generate_log_csv_row(log_dict: Dict[str, Any], log_columns: List[str]):
        log_dict["datetime"] = str(datetime.now())
        row = [log_dict[column] for column in log_columns]

        return row

    @staticmethod
    def write_to_csv(row: List[Any], file_path: str) -> None:
        with open(file_path, "a+") as log_csv:
            writer = csv.writer(log_csv, delimiter=",")
            writer.writerow(row)

    @staticmethod
    def read_files_in_dir(dir_path: str) -> List[str]:
        to_remove = [".DS_Store", ".ipynb_checkpoints", ".keep"]

        files = os.listdir(dir_path)
        return [item for item in files if item not in to_remove]
