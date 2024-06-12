import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import logging
import time
from utils import setup_logging, save_list_to_file, get_listing_ids, read_jsonl


LOG_FILE_PATH = "../../logs/parsing_listing_info.log"


def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Parse Airbnb listing house rules.')
    parser.add_argument('--output_path', type=str, default='../../data/sample_parce_listings',
                        help='Path to save the parsed house rules files')
    parser.add_argument('--data_path', type=str, default='../../data/download_test',
                        help='Path to the the folder containing downloaded listings jsonls')
    return parser.parse_args()


def parse_house_rules_json(listing_id: str, presentation: dict):
    house_rules_dict = {'listing_id': listing_id}

    try:
        sections = presentation['stayProductDetailPage']['sections']['sections']
    except Exception as ex:
        logging.error(f"Failed processing {listing_id}. {presentation=}. Error: {ex.with_traceback()}")
        return

    for section in sections:
        try:
            if section['section']['__typename'] == 'PoliciesSection':
                house_rules_section = section['section']
                logging.info(f"{listing_id} house_rules_section found")
        except:
            continue


    for house_rules_item in house_rules_section['houseRulesSections']:
        try:
            if house_rules_item['title']:
                house_rule_name = f"{house_rules_item['title'].lower().replace(' ', '_')}_house_rule"

                items_list = []

                for item in house_rules_item['items']:
                    if item['subtitle']:
                        items_list.append(': '.join([item['title'], item['subtitle']]))
                    else:
                        items_list.append(item['title'])

                house_rules_dict[house_rule_name] = items_list

                if item['title'] == 'Additional rules':
                    additional_rules_to_add_list = item['html']['htmlText']#.split('\n')
                    house_rules_dict[house_rule_name].append(additional_rules_to_add_list)

        except:
            continue
    return house_rules_dict


def get_listing_presentation(listing_info_json: object, listing_id: str) -> object:
    try:
        # Extract the presentation data
        presentation = listing_info_json[0]['root > core-guest-spa'][1][1]['niobeMinimalClientData'][1][1]['data']['presentation']
    except Exception as ex:
        logging.error(f"{listing_id=} can't get presentation. Error: {ex.with_traceback()}")
        return
    
    return presentation


def main():
    """
    Main function to parse Airbnb listing descriptions and save them to files.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging(LOG_FILE_PATH)

    logging.info(f"{args=}")

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    listing_id_json_list = [jsonl_filepath 
                            for jsonl_filepath in os.listdir(args.data_path) if jsonl_filepath.endswith('.jsonl')]
    logging.info(f"{len(listing_id_json_list)=}")

    output_file_path = os.path.join(args.output_path, 'house_rules.jsonl')

    # Loop through each listing ID and process it
    total_listings = len(listing_id_json_list)

    for count, listing_id_json_file in enumerate(listing_id_json_list, start=1):

        listing_id = listing_id_json_file.replace('.jsonl', '')
        logging.info(f"Starting {listing_id_json_file=}, {listing_id=} ({count}/{total_listings})")

        json_file_path = os.path.join(args.data_path, listing_id_json_file)
        
        # url = f"https://www.airbnb.com/rooms/{listing_id}"

        # response = requests.get(url)
        # if response.status_code != 200:
        #     logging.error(f"{listing_id=} failed to be scraped, {response.status_code=}")
        #     continue

        # html_content = response.text
        # soup = BeautifulSoup(html_content, 'html.parser')

        # # Find the specific script tag containing the JSON data
        # script_tag = soup.find('script', {'data-injector-instances': 'true', 'id': 'data-injector-instances', 'type': 'application/json'})
        
        # if not script_tag:
        #     logging.error(f"{listing_id} No matching script tag found. Listing ID does not exist")
        #     continue

        # # Parse the JSON data from the script tag
        # listing_info_json = json.loads(script_tag.text)

        listing_info_json = read_jsonl(json_file_path)

        # try:
        #     # Extract the presentation data
        #     presentation = listing_info_json['root > core-guest-spa'][1][1]['niobeMinimalClientData'][1][1]['data']['presentation']
        # except KeyError:
        #     logging.error(f"{listing_id} can't get presentation")
        #     return

        presentation = get_listing_presentation(listing_info_json, listing_id)

        # house_rules_dict
        house_rules_dict = parse_house_rules_json(listing_id, presentation)

        # Write the extracted data to the output file
        with open(output_file_path, 'a') as file:  # Open file in append mode
            file.write(json.dumps(house_rules_dict) + '\n')

        logging.info(f"{listing_id=} added")

        # time.sleep(0.5) # To limit throttling

if __name__ == '__main__':
    main()
