#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# 
# ---
# 
# ## Starter Code to Generate Random Geographic Coordinates and a List of Cities

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from scipy.stats import linregress

# Impor the OpenWeatherMap API key
from api_keys import weather_api_key

# Import citipy to determine the cities based on latitude and longitude
from citipy import citipy


# ### Generate the Cities List by Using the `citipy` Library

# In[2]:


# Empty list for holding the latitude and longitude combinations
lat_lngs = []

# Empty list for holding the cities names
cities = []

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# Create a set of random lat and lng combinations
lats = np.random.uniform(lat_range[0], lat_range[1], size=1500)
lngs = np.random.uniform(lng_range[0], lng_range[1], size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
print(f"Number of cities in the list: {len(cities)}")


# ---

# ## Requirement 1: Create Plots to Showcase the Relationship Between Weather Variables and Latitude
# 
# ### Use the OpenWeatherMap API to retrieve weather data from the cities list generated in the started code

# In[3]:


# Set the API base URL
url = f"http://api.openweathermap.org/data/2.5/weather?appid={weather_api_key}&q="

# Define an empty list to fetch the weather data for each city
city_data = []

# Print to logger
print("Beginning Data Retrieval     ")
print("-----------------------------")

# Create counters
record_count = 1
set_count = 1

# Loop through all the cities in our list to fetch weather data
for i, city in enumerate(cities):
#change the city everytime        
    # Group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0

    # Create endpoint URL with each city
    city_url = url + city
    
    # Log the url, record, and set numbers
    print("Processing Record %s of Set %s | %s" % (record_count, set_count, city))

    # Add 1 to the record count
    record_count += 1

    # Run an API request for each of the cities
    try:
        # Parse the JSON and retrieve data
        city_weather = requests.get(city_url).json()

        # Parse out latitude, longitude, max temp, humidity, cloudiness, wind speed, country, and date
        city_lat = city_weather["coord"]["lat"]
        city_lng = city_weather["coord"]["lon"]
        city_max_temp = city_weather["main"]["temp_max"]
        city_humidity = city_weather["main"]["humidity"]
        city_clouds = city_weather["clouds"]["all"]
        city_wind = city_weather["wind"]["speed"]
        city_country = city_weather["sys"]["country"]
        city_date = city_weather["dt"]

        # Append the City information into city_data list
        city_data.append({"City": city, 
                          "Lat": city_lat, 
                          "Lng": city_lng, 
                          "Max Temp": city_max_temp,
                          "Humidity": city_humidity,
                          "Cloudiness": city_clouds,
                          "Wind Speed": city_wind,
                          "Country": city_country,
                          "Date": city_date})

    # If an error is experienced, skip the city
    except:
        print("City not found. Skipping...")
        pass
              
# Indicate that Data Loading is complete 
print("-----------------------------")
print("Data Retrieval Complete      ")
print("-----------------------------")


# In[4]:


# Convert the cities weather data into a Pandas DataFrame
city_data_df = pd.DataFrame(city_data)

# Show Record Count
city_data_df.count()


# In[5]:


# Display sample data
city_data_df.head()


# In[6]:


# Export the City_Data into a csv
city_data_df.to_csv("World_Weather_Analysis.csv")


# In[7]:


# Read saved data
city_data_df = pd.read_csv("World_Weather_Analysis.csv", index_col="City")

# Display sample data
city_data_df.head()


# ### Create the Scatter Plots Requested
# 
# #### Latitude Vs. Temperature

# In[8]:


# Build scatter plot for latitude vs. temperature
plt.scatter(city_data_df["Lat"], city_data_df["Max Temp"], marker="o")
# Incorporate the other graph properties
plt.title("Lat vs. Temp")
plt.ylabel("Temp (Celsius)")
plt.xlabel("Lat")
plt.grid(True)

# Save the figure
plt.savefig

# Show plot
plt.show()



# #### Latitude Vs. Humidity

# In[9]:


# Build the scatter plots for latitude vs. humidity
plt.scatter(city_data_df["Lat"], city_data_df["Humidity"], marker="o")

# Incorporate the other graph properties
plt.title("Lat vs. Humidity" )
plt.ylabel("Temperature (Celsius)")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig

# Show plot
plt.show()


# #### Latitude Vs. Cloudiness

# In[10]:


# Build the scatter plots for latitude vs. cloudiness
plt.scatter(city_data_df["Lat"], city_data_df["Cloudiness"], marker="o")

# Incorporate the other graph properties
plt.title("Lat vs. Cloudiness")
plt.ylabel("Temperature (Celsius)")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[11]:


# Build the scatter plots for latitude vs. wind speed
plt.scatter(city_data_df["Lat"], city_data_df["Wind Speed"], marker="o")


# Incorporate the other graph properties
plt.title("Lat vs. Wind Speed")
plt.ylabel("Temperature (Celsius)")
plt.xlabel("Latitude")
plt.grid(True)

# Save the figure
plt.savefig

# Show plot
plt.show()


# ---
# 
# ## Requirement 2: Compute Linear Regression for Each Relationship
# 

# In[12]:


def plot_linear_regression(x_values, y_values, title, text_coordinates):
    
    # Compute linear regression
    (slope, intercept, rvalue, pvalue, stderr) = linregress(x_values, y_values)
    regress_values = x_values * slope + intercept
    line_eq = "y = " + str(round(slope,2)) + "x + " + str(round(intercept,2))

    # Plot
    plt.scatter(x_values,y_values)
    plt.plot(x_values,regress_values,"r-")
    plt.annotate(line_eq,text_coordinates,fontsize=15,color="red")
    plt.xlabel("Latitude")
    plt.ylabel(title)
    print(line_eq,text_coordinates)
    print(f"The r-value is: {rvalue**2}")
    plt.show()


 





# In[ ]:





# In[13]:


# Create a DataFrame with the Northern Hemisphere data (Latitude >= 0)
northern_hemi_df = city_data_df.loc[city_data_df['Lat']>=0]

northern_hemi_df.head()



# In[14]:


southern_hemi_df = city_data_df.loc[city_data_df['Lat']<=0]

southern_hemi_df.head()


# ###  Temperature vs. Latitude Linear Regression Plot

# In[15]:


x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values,"Temperature vs. Latitude", (50,50))


# In[ ]:





# In[16]:


x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Max Temp']
plot_linear_regression(x_values, y_values,"Temperature vs. Latitude", (50,50))


# **Discussion about the linear relationship:** from what I can see -- the 

# ### Humidity vs. Latitude Linear Regression Plot

# In[17]:


# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Humidity']
plot_linear_regression(x_values, y_values,"Humidity vs. Latitude", (50,50))


# In[18]:


# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Humidity']
plot_linear_regression(x_values, y_values,"Humidity vs. Latitude", (50,50))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# ### Cloudiness vs. Latitude Linear Regression Plot

# In[19]:


# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Cloudiness']
plot_linear_regression(x_values, y_values,"Cloudiness vs. Latitude", (50,50))


# In[20]:


# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Cloudiness']
plot_linear_regression(x_values, y_values,"Cloudiness vs. Latitude", (50,50))


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# ### Wind Speed vs. Latitude Linear Regression Plot

# In[21]:


# Northern Hemisphere
x_values = northern_hemi_df['Lat']
y_values = northern_hemi_df['Wind Speed']
plot_linear_regression(x_values, y_values,"Wind Speed vs. Latitude", (50,50))


# In[22]:


# Southern Hemisphere
x_values = southern_hemi_df['Lat']
y_values = southern_hemi_df['Wind Speed']
plot_linear_regression(x_values, y_values,"Wind Speed vs. Latitude", (50,50))


# In[23]:


#After each pair of plots, explain what the linear regression is modeling. Describe any relationships that you notice and any other findings you may uncover.


# **Discussion about the linear relationship:** YOUR RESPONSE HERE

# In[24]:


#After each pair of plots, explain what the linear regression is modeling. Describe any relationships that you notice and any other findings you may uncover.
#Cloudiness and lat -- are pretty close in by hemi's
#in southern and northern hemi -- the outcome came out almost as complete opposites in temp -- which I suppose isn't surprising
#the winds seem stronger in the south
#it is more cloudy in the north

# a very interesting layout of the different weather patterns -- it does give way to north and south weather trends and I think it's important to continue these study's to see how the weather changes over time


# In[ ]:




