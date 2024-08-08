#!/usr/bin/env python
# coding: utf-8

# # VacationPy
# ---
# 
# ## Starter Code to Import Libraries and Load the Weather and Coordinates Data

# In[1]:


# Dependencies and Setup
import hvplot.pandas
import pandas as pd
import requests

# Import API key
from api_keys import geoapify_key


# In[2]:


# Load the CSV file created in Part 1 into a Pandas DataFrame
city_data_df = pd.read_csv("World_Weather_Analysis.csv")

# Display sample data
city_data_df.head()


# ---
# 
# ### Step 1: Create a map that displays a point for every city in the `city_data_df` DataFrame. The size of the point should be the humidity in each city.

# In[4]:


all_city_map = city_data_df.hvplot.points(
    "Lng",
    "Lat",
    geo = True,
    tiles = "OSM",
    frame_width = 800,
    frame_height = 600,
    size = "Humidity",
    alpha = 0.5,
    color = "Country")

# Display the map
all_city_map

#


# ### Step 2: Narrow down the `city_data_df` DataFrame to find your ideal weather condition

# In[ ]:


# Narrow down cities that fit criteria and drop any results with null values
min_temp = 45
max_temp = 75

# Filter cities that meet the temperature criteria
filtered_cities_df = city_data_df[(city_data_df['Max Temp'] >= min_temp) & (city_data_df['Max Temp'] <= max_temp)]

# Drop rows with null values
filtered_cities_df = filtered_cities_df.dropna()

# Display the resulting DataFrame
filtered_cities_df


# ### Step 3: Create a new DataFrame called `hotel_df`.

# In[ ]:


# Create an empty DataFrame to store hotel data
hotel_data_df = pd.DataFrame(city_data_df)

# Add an empty "Hotel Name" column to the DataFrame
hotel_data_df['Hotel Name'] = ''

# Display sample data
print(hotel_data_df.head())  


# ### Step 4: For each city, use the Geoapify API to find the first hotel located within 10,000 metres of your coordinates.

# In[ ]:


# Set parameters to search for a hotel
radius = 10000
params = {
    "categories":"accommodation.hotel",
    "apiKey": geoapify_key,
    "limit":20
}

# Print a message to follow up the hotel search
print("Starting hotel search")

# Iterate through the hotel_data_df DataFrame
for index, row in hotel_data_df.iterrows():
    # get latitude, longitude from the DataFrame
    latitude = row["Lat"]
    longitude = row["Lng"]
    
    # Add the current city's latitude and longitude to the params dictionary
    params["filter"] = f"circle:{longitude},{latitude},{radius}"
    params["bias"] = f"proximity:{longitude},{latitude}"
    
    # Set base URL
    base_url = "https://api.geoapify.com/v2/places"

    # Make and API request using the params dictionaty
    name_address = requests.get(base_url, params=params)
    
    # Convert the API response to JSON format
    name_address = name_address.json()
    
    # Grab the first hotel from the results and store the name in the hotel_df DataFrame
    try:
        hotel_data_df.loc[index, "Hotel Name"] = name_address["features"][0]["properties"]["name"]
    except (KeyError, IndexError):
        # If no hotel is found, set the hotel name as "No hotel found".
        hotel_data_df.loc[index, "Hotel Name"] = "No hotel found"
        
    # Log the search results
    print(f"{hotel_data_df.loc[index, 'City']} - nearest hotel: {hotel_data_df.loc[index, 'Hotel Name']}")

# Display sample data
hotel_data_df

















# ### Step 5: Add the hotel name and the country as additional information in the hover message for each city in the map.

# In[ ]:


hotel_map = city_data_df.hvplot.points(
    "Lng",
    "Lat",
    geo = True,
    tiles = "OSM",
    frame_width = 800,
    frame_height = 600,
    size = "Humidity",
    scale = 1,
    color = "City",
    hover_cols = ["Hotel Name", "Country"]
)

hotel_map



# In[ ]:





# In[ ]:




