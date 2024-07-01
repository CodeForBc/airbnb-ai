# import jsonl file to mongoDB

import json
import os
import sys
import argparse 


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

def import_jsonl_to_mongo(args):
    
    uri = f"mongodb+srv://{args.username}:{args.password}@airbnb-listings.igjyxzf.mongodb.net/?appName=airbnb-listings"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[args.db_name]
    collection = db[args.collection_name]

    with open(args.jsonl_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            collection.insert_one(data)

    print('Imported data from {} to {}.{}'.format(args.jsonl_file, args.db_name, args.collection_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import jsonl file to mongoDB')
    parser.add_argument('--jsonl_file', type=str, help='jsonl file to import', default='~/Downloads/raw_data_descriptions_amenities_house_rules (1).jsonl')
    parser.add_argument('--db_name', type=str, help='db name')
    parser.add_argument('--collection_name', type=str, help='collection name')
    parser.add_argument('--username', type=str, help='your mongoDB usernane')
    parser.add_argument('--password', type=str, help='your mongoDB password')

    args = parser.parse_args()
    import_jsonl_to_mongo(args.jsonl_file, args.db_name, args.collection_name)

