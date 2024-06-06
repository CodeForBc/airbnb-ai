import os
from dotenv import load_dotenv
import requests
import time
import csv
import logging

# Configure logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../../logs/airbnb_data_collection.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables from .env file
load_dotenv('../../.env')

API_KEY = os.getenv('RAPIDAPI_KEY')

# Constants
API_HOST = "airbnb13.p.rapidapi.com"
BASE_URL = "https://airbnb13.p.rapidapi.com/search-geo"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST,
    "Content-Type": "application/json"
}

QUERYSTRING = {
    "location": "Squamish, BC, Canada",  # Change city here
    "checkin": "2024-07-01",  # Change for different dump
    "checkout": "2024-07-04",  # Change for different dump
    "adults": "1",
    "children": "0",
    "infants": "0",
    "pets": "0",
    "page": "1",
    "currency": "CAD"
}

DATA_FILENAME = f'../../data/raw_data/airbnb_results_{QUERYSTRING["checkin"]}_{QUERYSTRING["checkout"]}.csv'


def make_request(page):
    """
    Make the API request for the given page.
    """
    QUERYSTRING['page'] = page
    response = requests.get(BASE_URL, headers=HEADERS, params=QUERYSTRING)
    response.raise_for_status()  # Check for request errors
    return response.json()


def extract_data(result):
    """
    Extract and flatten the relevant data from the result.
    """
    try:
        price = result.get('price', {})
        return {
            'id': result.get('id', ''),
            'userId': result.get('userId', ''),
            'name': result.get('name', ''),
            'address': result.get('address', ''),
            'city': result.get('city', ''),
            'isSuperhost': result.get('isSuperhost', False),
            'lat': result.get('lat', ''),
            'lng': result.get('lng', ''),
            'persons': result.get('persons', 0),
            'rating': result.get('rating', 0.0),
            'reviewsCount': result.get('reviewsCount', 0),
            'type': result.get('type', ''),
            'cancelPolicy': result.get('cancelPolicy', ''),
            'deeplink': result.get('deeplink', ''),
            'hostThumbnail': result.get('hostThumbnail', ''),
            'price_currency': price.get('currency', ''),
            'price_rate': price.get('rate', 0),
            'price_total': price.get('total', 0),
            'bathrooms': result.get('bathrooms', 0),
            'bedrooms': result.get('bedrooms', 0),
            'beds': result.get('beds', 0),
            'previewAmenities': ', '.join(result.get('previewAmenities', [])),
            'url': result.get('url', ''),
            'images': result.get('images', []),
            'amenityIds': result.get('amenityIds', [])
        }
    except KeyError as e:
        logging.error(f"Missing key in result: {e}")
        logging.error("Result data: %s", result)
        return {}


def save_results(new_results, is_first_write):
    """
    Save the new results to the CSV file.
    """
    fieldnames = [
        'id', 'userId', 'name', 'address', 'city', 'isSuperhost', 'lat', 'lng', 'persons',
        'rating', 'reviewsCount', 'type', 'cancelPolicy', 'deeplink', 'hostThumbnail',
        'price_currency', 'price_rate', 'price_total', 'bathrooms', 'bedrooms',
        'beds', 'previewAmenities', 'url', 'images', 'amenityIds'
    ]
    
    with open(DATA_FILENAME, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if is_first_write:
            writer.writeheader()
        for result in new_results:
            data = extract_data(result)
            if data:
                writer.writerow(data)


def main():
    seen_ids = set()
    page = 1
    is_first_write = True

    while True:
        logging.info(f"Fetching page {page}...")
        data = make_request(page)
        results = data.get('results', [])
        if not results:
            break

        new_results = [result for result in results if result['id'] not in seen_ids]

        if not new_results:
            logging.info("Duplicate results detected. Stopping.")
            break

        for result in new_results:
            seen_ids.add(result['id'])

        save_results(new_results, is_first_write)
        is_first_write = False

        page += 1
        time.sleep(61)  # Ensure no more than 1 request per minute (RapidAPI free tier limit)

    logging.info("Data collection completed.")

if __name__ == "__main__":
    main()
