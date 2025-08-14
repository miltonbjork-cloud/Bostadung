import os
from glob import glob

def get_raw_list_file_path(queue, year, building_type, group):
    return os.path.join("data", "raw_lists", f"{queue}_{year}_{building_type}_{group}.json")

def get_all_raw_list_files():
    return glob(os.path.join("data", "raw_lists", "*.json"))
