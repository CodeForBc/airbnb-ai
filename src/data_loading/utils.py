import logging
import json
import os
import pandas as pd
from typing import List


def setup_logging(logfile_path: str):
    """
    Setup logging configuration to log messages to both a file and the console.

    Args:
        logfile_path (str): Path to the log file where log messages will be saved.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(logfile_path),
                            logging.StreamHandler()
                        ])
    

def save_list_to_file(file_name: str, data_list: List, path: str):
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
    """
    Retrieve listing IDs from a CSV file.

    Args:
        data_path (str): Path to the CSV file containing listing data.

    Returns:
        List[int]: A list of listing IDs extracted from the CSV file.
    """
    data_id = pd.read_csv(data_path)
    logging.info(f"{data_id.shape=}")
    listing_id_list = data_id.id.values

    return listing_id_list


def read_jsonl(file_path: str) -> List[dict]:
    """
    Read a JSON Lines file and return its contents as a list of dictionaries.

    Args:
        file_path (str): Path to the JSON Lines file.

    Returns:
        List[dict]: A list of dictionaries representing the contents of the JSON Lines file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        json_list = [json.loads(line) for line in lines]
    return json_list
