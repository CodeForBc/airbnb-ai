import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import argparse
import logging
import time


def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Parse Airbnb listing house rules.')
    parser.add_argument('--description_parsing_path', type=str, default='../../data/description_parsing_amenities',
                        help='Path to save the parsed house rules files')
    parser.add_argument('--data_path', type=str, default='../../data/raw_data/raw_data_Anna.csv',
                        help='Path to the CSV file containing listing IDs')
    return parser.parse_args()


def setup_logging():
    """
    Setup logging configuration to log messages to both a file and the console.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("../../logs/description_parsing_amenities.log"),
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


def main():
    """
    Main function to parse Airbnb listing descriptions and save them to files.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging()

    # Create the output directory if it doesn't exist
    if not os.path.exists(args.description_parsing_path):
        os.makedirs(args.description_parsing_path)

    # Read the input data
    data_id = pd.read_csv(args.data_path)
    logging.info(f"Data shape: {data_id.shape}")

    listing_id_list = data_id.id.values
    output_file_path = os.path.join(args.description_parsing_path, 'description_parsing_amenities.jsonl')

    # Initialize lists to store error information
    listing_description_list = []
    cannot_get_presentation_list = []
    cannot_get_selected_sections_list = []
    cannot_get_item_from_selected_section_list = []
    listing_does_not_exist_no_matching_script_tag_list = []
    cannot_get_amenities_sections_list = []

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
            listing_does_not_exist_no_matching_script_tag_list.append(listing_id)
            continue

        # Parse the JSON data from the script tag
        listing_info_json = json.loads(script_tag.text)

        try:
            # Extract the presentation data
            presentation = listing_info_json['root > core-guest-spa'][1][1]['niobeMinimalClientData'][1][1]['data']['presentation']
        except KeyError:
            logging.error(f"{listing_id} can't get presentation")
            cannot_get_presentation_list.append(listing_id)
            continue

       
        amenities_dict = {'listing_id': listing_id}

        try:
            sections = presentation['stayProductDetailPage']['sections']['sections']
        except:
            cannot_get_selected_sections_list.append(listing_id)
            continue


        for section in sections:
            try:
                if section['section']['__typename'] == 'AmenitiesSection':
                    amenities_section = section['section']  
            except:
                continue
        
        if 'seeAllAmenitiesGroups' not in amenities_section.keys():
            cannot_get_amenities_sections_list.append(listing_id)
            continue


        for amenity_item in amenities_section['seeAllAmenitiesGroups']:
            try:
                if amenity_item['title']:
                    amenity_name = f"{amenity_item['title'].lower().replace(' ', '_')}_amenities"
                    amenities_dict[amenity_name] = [item['title'] for item in amenity_item['amenities']]
            except:
                continue

        # Write the extracted data to the output file
        with open(output_file_path, 'a') as file:  # Open file in append mode
            file.write(json.dumps(amenities_dict) + '\n')

        logging.info(f"{listing_id} added")

        time.sleep(0.5) # To limit throttling

    # Save error lists to files
    save_list_to_file('cannot_get_presentation_list.txt', cannot_get_presentation_list, args.description_parsing_path)
    save_list_to_file('cannot_get_selected_sections_list.txt', cannot_get_selected_sections_list, args.description_parsing_path)
    save_list_to_file('cannot_get_item_from_selected_section_list.txt', cannot_get_item_from_selected_section_list, args.description_parsing_path)
    save_list_to_file('listing_does_not_exist_no_matching_script_tag_list.txt', listing_does_not_exist_no_matching_script_tag_list, args.description_parsing_path)
    save_list_to_file('cannot_get_amenities_sections_list.txt', cannot_get_amenities_sections_list, args.description_parsing_path)


if __name__ == '__main__':
    main()
