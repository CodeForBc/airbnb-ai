import logging
import json
import os
import argparse
import pandas as pd
from typing import List


def setup_logging(logfile_path: str):
    """
    Setup logging configuration to log messages to both a file and the console.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(logfile_path),
                            logging.StreamHandler()
                        ])
    

def save_list_to_file(file_name, data_list, path):
    """
    Save a list of data to a specified file.

    Args:
        file_name (str): Name of the file to save the data.
        data_list (list): List of data to save.
        path (str): Directory path where the file will be saved.
    """
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as file:
        file.write(json.dumps(data_list))


def get_listing_ids(data_path: str) -> List[int]:
    data_id = pd.read_csv(data_path)
    logging.info(f"{data_id.shape=}")
    listing_id_list = data_id.id.values

    return listing_id_list


# Method to read the JSON Lines file
def read_jsonl(file_path: str) -> List[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        json_list = [json.loads(line) for line in lines]
    return json_list
