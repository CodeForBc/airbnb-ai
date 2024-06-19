import json
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import setup_logging, get_listing_ids
import logging
import argparse
from typing import List 
import time


LOG_FILE_PATH = "../../logs/download_listing_jsons.log"


def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Download Airbnb listing html and save json part of them.')
    parser.add_argument('--path_to_save', type=str, default='../../data/listing_page_jsons',
                        help='Path to save json part of Airbnb listing html')
    parser.add_argument('--data_path', type=str, default='../../data/raw_data/raw_data_Anna.csv',
                        help='Path to the CSV file containing listing IDs')
    return parser.parse_args()


def main():
    """
    Main function to parse Airbnb listing descriptions and save them to files.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging(LOG_FILE_PATH)

    logging.info(f"{args=}")

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.path_to_save):
        os.makedirs(args.path_to_save)

    listing_id_list = get_listing_ids(args.data_path)
    logging.info(f"{len(listing_id_list)=}")

    total_listings = len(listing_id_list)

    already_added_listing_ids = set([listing_id[:-6] 
                                     for listing_id in os.listdir(args.path_to_save) 
                                     if listing_id.endswith('.jsonl')])
    
    print(f'{already_added_listing_ids=}')

    for count, listing_id in enumerate(listing_id_list, start=1):
        listing_id = str(listing_id)

        logging.info(f"Starting {listing_id=} ({count}/{total_listings})")

        if listing_id in already_added_listing_ids:
            logging.info(f"{listing_id=} already exists")
            continue
        
        url = f"https://www.airbnb.com/rooms/{listing_id}"

        response = requests.get(url)

        if response.status_code != 200:
            logging.error(f"{listing_id=} failed to be scraped, {response.status_code=}")
            continue

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specific script tag containing the JSON data
        script_tag = soup.find('script', {'data-injector-instances': 'true', 'id': 'data-injector-instances', 'type': 'application/json'})
        
        if not script_tag:
            # logging.warning(f"{listing_id} No matching script tag found. Listing ID does not exist")
            logging.error(f"{listing_id=} No matching script tag found")
            continue

        # Parse the JSON data from the script tag
        listing_info_json = json.loads(script_tag.text)

        output_file_path = os.path.join(args.path_to_save, listing_id + '.jsonl')

        # Write the extracted data to the output file
        with open(output_file_path, 'w') as file:  
            file.write(json.dumps(listing_info_json) + '\n')

        logging.info(f"{listing_id=} saved to {output_file_path=}")

        time.sleep(0.2)


if __name__ == '__main__':
    main()
