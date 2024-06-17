# Ensure you have the geopy package installed
# Run the following command in your terminal or command prompt to install geopy:
# pip install geopy

import pandas as pd
import os
from geopy.distance import geodesic

# Verify the current working directory
print("Current working directory:", os.getcwd())

# List files in the directory to verify the file exists
print("Files in directory:", os.listdir(r'D:\airbnb-ai\data\raw_data'))

# Load the CSV file using an absolute path
file_path = r'D:\airbnb-ai\data\raw_data\Xavier_rawdata_2024-07-08_Kelowna_Chilliwack_Abbotsford.csv'
df = pd.read_csv(file_path)

# Print the column names to verify
print("Column names in the CSV file:", df.columns)

# Add new columns for latitude and longitude directly from the 'Lat' and 'lng' columns
df['latitude'] = df['lat']
df['longitude'] = df['lng']

# Function to calculate distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

# Identify listings by the same owner that are less than 100 meters apart and combine listing IDs into arrays
def find_nearby_listings_combined(df):
    results = []
    owners = df['userId'].unique()
    
    for owner in owners:
        owner_listings = df[df['userId'] == owner]
        
        combined_listings = []
        for i, listing1 in owner_listings.iterrows():
            for j, listing2 in owner_listings.iterrows():
                if i >= j:  # Avoid duplicate and self-comparison
                    continue
                
                distance = calculate_distance(listing1['latitude'], listing1['longitude'], listing2['latitude'], listing2['longitude'])
                if distance < 100:
                    combined_listings.append({
                        'listing1 ID': listing1['id'],
                        'listing2 ID': listing2['id'],
                        'distance (meters)': distance
                    })
        
        if combined_listings:
            listing_ids = list(set([item for sublist in [[d['listing1 ID'], d['listing2 ID']] for d in combined_listings] for item in sublist]))
            avg_distance = sum([d['distance (meters)'] for d in combined_listings]) / len(combined_listings)
            results.append({
                'userId': owner,
                'host_listing_ids': listing_ids,
                'average_distance (meters)': avg_distance
            })
    
    return pd.DataFrame(results)

# Calculate the total number of listings and the number of listings more than 100 meters apart
def calculate_host_listings_info(df):
    host_info = []
    owners = df['userId'].unique()
    
    for owner in owners:
        owner_listings = df[df['userId'] == owner]
        total_listings = len(owner_listings)
        
        for i, listing1 in owner_listings.iterrows():
            distant_listings = 0
            for j, listing2 in owner_listings.iterrows():
                if i == j:
                    continue
                
                distance = calculate_distance(listing1['latitude'], listing1['longitude'], listing2['latitude'], listing2['longitude'])
                if distance > 100:
                    distant_listings += 1
            
            host_info.append({
                'host_id': owner,
                'listing_id': listing1['id'],
                'n_host_listings_total': total_listings,
                'n_host_listings_different_location': distant_listings
            })
    
    return pd.DataFrame(host_info)

# Save the DataFrame to a CSV file
def save_dataframe_to_file(file_name, dataframe, path):
    """
    Save a DataFrame to a specified CSV file.

    Args:
        file_name (str): Name of the file to save the data.
        dataframe (pd.DataFrame): DataFrame to save.
        path (str): Directory path where the file will be saved.
    """
    file_path = os.path.join(path, file_name)
    dataframe.to_csv(file_path, index=False)

# Error handling and saving problematic listing IDs
def handle_errors_and_save(problematic_ids, file_name, path):
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as file:
        for listing_id in problematic_ids:
            file.write(f"{listing_id}\n")

# Get the results with combined listing IDs
try:
    combined_listings_df = find_nearby_listings_combined(df)
except Exception as e:
    handle_errors_and_save(df['id'], 'problematic_listings.txt', r'D:\airbnb-ai\data\raw_data')
    raise e

# Calculate host listings information
try:
    host_listings_info_df = calculate_host_listings_info(df)
except Exception as e:
    handle_errors_and_save(df['id'], 'problematic_listings.txt', r'D:\airbnb-ai\data\raw_data')
    raise e

# Specify the output file name and path
output_file_name_combined = 'combined_listings.csv'
output_file_name_host_info = 'host_listings_info.csv'
output_path = r'D:\airbnb-ai\data\raw_data'

# Save the results to CSV files
save_dataframe_to_file(output_file_name_combined, combined_listings_df, output_path)
save_dataframe_to_file(output_file_name_host_info, host_listings_info_df, output_path)

# Display the results in the console
print("Combined Listings:")
print(combined_listings_df)

print("\nHost Listings Info:")
print(host_listings_info_df)
