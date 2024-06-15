import pandas as pd
from geopy.distance import geodesic

# Load the CSV file
file_path = 'path_to_your_csv_file.csv'
df = pd.read_csv(file_path)

# Assuming the 'locations of each rental' column contains latitude and longitude in the format 'lat, lon'
def parse_location(location):
    lat, lon = map(float, location.split(','))
    return lat, lon

# Add new columns for latitude and longitude
df[['latitude', 'longitude']] = df['locations of each rental'].apply(parse_location).apply(pd.Series)

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

# Identify listings by the same owner that are less than 100 metres apart
def find_nearby_listings(df):
    results = []
    owners = df['owner ID'].unique()
    
    for owner in owners:
        owner_listings = df[df['owner ID'] == owner]
        
        for i, listing1 in owner_listings.iterrows():
            for j, listing2 in owner_listings.iterrows():
                if i >= j:  # Avoid duplicate and self-comparison
                    continue
                
                distance = calculate_distance(listing1['latitude'], listing1['longitude'], listing2['latitude'], listing2['longitude'])
                if distance < 100:
                    results.append({
                        'owner ID': owner,
                        'listing1 ID': listing1['Listing ID'],
                        'listing2 ID': listing2['Listing ID'],
                        'distance (meters)': distance
                    })
    
    return pd.DataFrame(results)

# Get the results
nearby_listings_df = find_nearby_listings(df)

# Display the results
import ace_tools as tools; tools.display_dataframe_to_user(name="Nearby Listings", dataframe=nearby_listings_df)
