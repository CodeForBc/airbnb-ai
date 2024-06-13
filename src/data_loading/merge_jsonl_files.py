import json
import pandas as pd
import os
import argparse
import logging
import glob

def parse_arguments():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(description='Parse Airbnb listing descriptions.')
    parser.add_argument('--description_parsing_path', type=str, default='../../data/description_parsing',
                        help='Path to save the parsed description files')
    parser.add_argument('--data_path', type=str, default='../../data/raw_data/raw_data.csv',
                        help='Path to the CSV file containing listing IDs')
    return parser.parse_args()


def setup_logging():
    """
    Setup logging configuration to log messages to both a file and the console.
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("../../logs/description_parsing.log"),
                            logging.StreamHandler()
                        ])

def read_jsonl(file_path):
    """Read a JSONL file and return a list of dictionaries."""
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]

def write_jsonl(data, output_path):
    """Write a list of dictionaries to a JSONL file."""
    with open(output_path, 'w') as file:
        for record in data.values():
            json.dump(record, file)
            file.write('\n')

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

def merge_jsonl_files(jsonl_files):
    """Merge multiple JSONL files based on a listing_id."""
    merged_data = {}
    
    for file_path in jsonl_files:
        records = read_jsonl(file_path)
        for record in records:
            listing_id = record['listing_id']
            if listing_id not in merged_data:
                merged_data[listing_id] = {}
            merged_data[listing_id].update(record)
    
    return merged_data

def extract_accomodation_types(output_file_path, data):
    """Extract accomodation types from data and save it in jsonl file"""
    for idx, row in data.iterrows():
        accomodation_type = {'listing_id': str(row['id']), 'accomodation_type': row['type']}
        # Write the extracted data to the output file
        with open(output_file_path, 'a') as file:  # Open file in append mode
            file.write(json.dumps(accomodation_type) + '\n')

def main():
    """
    Main function to extract Airbnb raw data, listing descriptions, accomodation type, amenities, house rules and host information. Outputs JSON response.
    """
    # Parse command-line arguments
    args = parse_arguments()
    setup_logging()

    # Extract data from csv
    data = pd.read_csv(args.data_path)[['id','type']]
    
    logging.info(f"data type: {data.shape}")

    # Extracting and saving new accomodation types jsonl
    output_file_path = os.path.join(args.description_parsing_path, 'accomodation_types.jsonl')
    extract_accomodation_types(output_file_path, data)

    # Merging all jsonl into one jsonl
    file_paths = glob.glob('../../data/description_parsing/*.jsonl')
    merged_data = merge_jsonl_files(file_paths)

    output_file = os.path.join(args.description_parsing_path, 'result.jsonl')
    write_jsonl(merged_data, output_file)
    
    logging.info(f"Merged data written to {output_file}")

if __name__ == '__main__':
    main()