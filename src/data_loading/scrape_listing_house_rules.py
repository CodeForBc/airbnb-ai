import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import logging
import time
from utils import setup_logging, save_list_to_file


def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Parse Airbnb listing house rules.')
    parser.add_argument('--description_parsing_path', type=str, default='../../data/description_parsing_house_rules',
                        help='Path to save the parsed house rules files')
    parser.add_argument('--data_path', type=str, default='../../data/raw_data/raw_data_Anna.csv',
                        help='Path to the CSV file containing listing IDs')
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


                # if house_rules_item['items']['title'] == 'Additional rules':
                #     additional_rules_to_add_list = house_rules_item['html']['htmlText'].split('\n')
                #     house_rules_dict[house_rule_name].extend(additional_rules_to_add_list)

            except:
                continue
        return house_rules_dict


def main():
    """
    Main function to parse Airbnb listing descriptions and save them to files.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging("../../logs/description_parsing_house_rules.log")

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.description_parsing_path):
        os.makedirs(args.description_parsing_path)

    # Read the input data
    data_id = pd.read_csv(args.data_path)
    logging.info(f"Data shape: {data_id.shape}")

    listing_id_list = data_id.id.values
    output_file_path = os.path.join(args.description_parsing_path, 'description_parsing_house_rules.jsonl')

    # Loop through each listing ID and process it
    total_listings = len(listing_id_list)
    for count, listing_id in enumerate(listing_id_list, start=1):
        listing_id = str(listing_id)
        logging.info(f"Starting listing_id={listing_id} ({count}/{total_listings})")
        
        url = f"https://www.airbnb.com/rooms/{listing_id}"

        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the specific script tag containing the JSON data
        script_tag = soup.find('script', {'data-injector-instances': 'true', 'id': 'data-injector-instances', 'type': 'application/json'})
        
        if not script_tag:
            logging.warning(f"{listing_id} No matching script tag found. Listing ID does not exist")
            continue

        # Parse the JSON data from the script tag
        listing_info_json = json.loads(script_tag.text)

        try:
            # Extract the presentation data
            presentation = listing_info_json['root > core-guest-spa'][1][1]['niobeMinimalClientData'][1][1]['data']['presentation']
        except KeyError:
            logging.error(f"{listing_id} can't get presentation")
            return

        # house_rules_dict
        house_rules_dict = parse_house_rules_json(listing_id, presentation)

        # Write the extracted data to the output file
        with open(output_file_path, 'a') as file:  # Open file in append mode
            file.write(json.dumps(house_rules_dict) + '\n')

        logging.info(f"{listing_id} added")

        time.sleep(0.5) # To limit throttling

if __name__ == '__main__':
    main()
