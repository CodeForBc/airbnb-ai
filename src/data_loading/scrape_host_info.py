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

# Identify listings by the same owner that are less than 100 metres apart
def find_nearby_listings(df):
    results = []
    owners = df['userId'].unique()
    
    for owner in owners:
        owner_listings = df[df['userId'] == owner]
        
        for i, listing1 in owner_listings.iterrows():
            for j, listing2 in owner_listings.iterrows():
                if i >= j:  # Avoid duplicate and self-comparison
                    continue
                
                distance = calculate_distance(listing1['latitude'], listing1['longitude'], listing2['latitude'], listing2['longitude'])
                if distance < 100:
                    results.append({
                        'userId': owner,
                        'listing1 ID': listing1['id'],
                        'listing2 ID': listing2['id'],
                        'distance (meters)': distance
                    })
    
    return pd.DataFrame(results)

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

# Get the results
nearby_listings_df = find_nearby_listings(df)

# Display the results in the console
print(nearby_listings_df)
#import ace_tools as tools; tools.display_dataframe_to_user(name="Nearby Listings", dataframe=nearby_listings_df)

# Specify the output file name and path
output_file_name = 'nearby_listings.csv'
output_path = r'D:\airbnb-ai\data\raw_data'

# Save the results to a CSV file
save_dataframe_to_file(output_file_name, nearby_listings_df, output_path)