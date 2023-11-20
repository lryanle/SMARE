# %%
%%javascript
IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
}

# %%
# import necessary libraries
import pandas as pd
import numpy as np
import math
import seaborn as sns
import datetime
import matplotlib.pylab as plt
import plotly.graph_objects as go
from pathlib import Path
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from matplotlib.ticker import NullFormatter
import matplotlib.ticker as ticker
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, DotProduct, RBF
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
%matplotlib inline

# %%
from pymongo import MongoClient
# MongoDB Atlas connection string
# Replace '<your_connection_string>' with your actual connection string
connection_string = '<your_connection_string>'

# Connect to MongoDB Atlas
client = MongoClient(connection_string)

# Specify the database and collection
# Replace '<your_database>' and '<your_collection>' with your actual database and collection names
database_name = '<your_database>'
collection_name = '<your_collection>'
db = client[database_name]
collection = db[collection_name]

# Fetch data from MongoDB and convert it to a DataFrame
cursor = collection.find()
data = list(cursor)
cars = pd.DataFrame(data)

# Convert DataFrame to CSV
csv_filename = 'output_data.csv'
cars.to_csv(csv_filename, index=False)

# Close the MongoDB connection
client.close()

print(f'Data has been successfully exported to {csv_filename}')


# %%
cars = pd.read_csv('output_data.csv')

# %%
#cars = pd.read_csv('data.csv')

# %%
cars.head()

# %%
cars.shape[0]

# %% [markdown]
# ## Data Cleaning

# %%
# drop unnecessary variables: id, url, region_url, VIN, image_url, description, lat, and long
cars = cars.drop(columns = ['_id', 'link'])

# %%
cars.head()

# %%
# look at the number of NA values by column
cars.isna().sum()

# %%
cars = cars.drop(columns = ['images/23','images/22','images/21','images/20','images/19','images/18','images/17','images/16','images/15','images/14','images/13','images/12','images/11','images/10','images/9','images/8', 'images/7','images/6','images/5','images/4','images/3','images/2','images/1'])

# %%
cars.head()

# %%
cars.shape[0]

# %%
# drop NA values
cars = cars.dropna()

# %%
cars.shape[0]

# %%
cars.head()

# %%
# convert year and odometer to integer values
#cars['odometer'] = cars['odometer'].str.replace('K', '').str.replace(' miles', '').astype(int) * 1000
#cars['odometer'] = cars['odometer'].str.replace('K miles', '').str.replace(' miles · Dealership', '').astype(float).astype(int) * 1000
import re
cars['odometer'] = cars['odometer'].apply(lambda x: int(re.search(r'\d+', str(x)).group(0)) if re.search(r'\d+', str(x)) else None)
cars['year'] = cars['title'].str.extract(r'(\d{4})')
# Fill NaN values in the 'year' column with a placeholder (you can choose a value that makes sense)
cars['year'].fillna(-1, inplace=True)
cars = cars.astype({'year':'int', 'odometer':'int'})

# %%
# create an age variable to get a better understanding of how old a car is
cars['age'] = datetime.date.today().year - cars['year']

# %%
cars.head()

# %% [markdown]
# ## Data Exploration

# %%
sns.histplot(data = cars, x = 'age', binwidth = 5).set(title = 'Distribution of Car Ages')

# %%
cars[cars['year'] < 1990]

# %%
cars = cars[cars.year >= 2005]

# %%
cars.shape[0]

# %%
# looking again at the distribution of ages
sns.histplot(data = cars, x = 'age', binwidth = 1).set(title = 'Distribution of Car Ages')

# %%
cars.shape[0]

# %%
sns.histplot(data = cars, x = 'odometer').set(title = 'Distribution of Car Odometer')

# %%
cars[cars['odometer'] > 300]

# %%
cars = cars[cars.odometer <= 300]
# Clean up the 'price' column by replacing non-numeric values with NaN
cars['price'] = pd.to_numeric(cars['price'].replace('[\$,]', '', regex=True), errors='coerce')

# Fill NaN values in the 'price' column with a placeholder (you can choose a value that makes sense)
cars['price'].fillna(-1, inplace=True)

# Convert 'price' column to integers
cars['price'] = cars['price'].astype(int)


# %%
cars.shape[0]

# %%
sns.histplot(data = cars, x = 'odometer').set(title = 'Distribution of Car Odometer')

# %%
sns.scatterplot(data = cars, x = 'odometer', y = 'price').set(title = 'Correlation of Vehicle Odometer and List Price')

# %%
cars[cars['price'] > 100000]

# %%
cars = cars[cars.price <= 100000]

# %%
cars.shape[0]

# %%
# look at the odometer vs price now
sns.scatterplot(data = cars, x = 'odometer', y = 'price').set(title = 'Correlation of Vehicle Odometer and List Price')

# %%
sns.histplot(data = cars, x = 'price').set(title = 'Distribution of List Price')

# %%
cars[cars['price'] < 1000]

# %%
cars = cars[cars.price >= 1000]

# %%
sns.histplot(data = cars, x = 'price').set(title = 'Distribution of List Price')

# %%
cars.shape[0]

# %%
#Dictionary of car makes
kbb_make = {
    'acura',
    'alfa-romeo',
    'aston-martin',
    'audi',
    'bentley',
    'bmw',
    'buick',
    'cadillac',
    'chevrolet',
    'chrysler',
    'dodge',
    'ferrari',
    'fiat',
    'ford',
    'genesis',
    'gmc',
    'honda',
    'hyundai',
    'infiniti',
    'jaguar',
    'jeep',
    'kia',
    'lamborghini',
    'land rover',
    'lexus',
    'lincoln',
    'lucid',
    'maserati',
    'mazda',
    'mclaren',
    'mercedes-benz',
    'mini',
    'mitsubishi',
    'nissan',
    'polestar',
    'porsche',
    'ram',
    'rivian',
    'rolls-royce',
    'subaru',
    'tesla',
    'toyota',
    'volkswagen',
    'volvo',
}

# Dictionary to store car models for each make
kbb_models = {
    'acura': ['ILX', 'MDX', 'NSX','RDX','TLX'],
    'alfa-romeo': ['Giulia', 'Stelvio'],
    'aston-martin': ['DB11', 'DBS', 'DBX','Vantage'],
    'audi': ['A3', 'A4','A4 allroad','A5', 'A6','A6 allroad',
             'A7','A8','e-tron','e-tron GT','e-tron S',
             'e-tron S Sportback','e-tron Sportback','Q3',
             'Q4 e-tron','Q4 Sportback e-tron','Q5', 
             'Q5 Sportback','Q7','Q8','R8','RS 3','RS 5',
             'RS 6','RS 7', 'RS e-tron GT','RS Q8','S3',
             'S4','S5','S6','S7','S8','SQ5','SQ5 Sportback',
             'SQ7','SQ8','TT'],
    'bentley': ['Bentayga','Continental GT','Flying Spur'],
    'bmw': ['2 Series','3 Series','4 Series', '5 Series',
            '6 Series','7 Series','8 Series','i4','iX','M3',
            'M4','M5','M8','X1','X2','X3','X3 M','X4','X4 M','X5',
            'X5 M','X6','X6 M','X7','Z4'],
    'buick': ['Enclave','Encore','Encore GX','Envision'],
    'cadillac': ['CT4','CT5','Escalade','Escalade ESV','XT4','XT5','XT6'],
    'chevrolet': ['Blazer','Bolt EUV','Bolt EV','Camaro','Colorado Crew Cab',
                  'Colorado Extended Cab','Corvette','Equinox','Express 2500 Cargo',
                  'Express 2500 Passenger','Express 3500 Cargo','Express 3500 Passenger',
                  'Malibu','Silverado 1500 Crew Cab','Silverado 1500 Double Cab',
                  'Silverado 1500 Regular Cab','Silverado 1500 Limited Crew Cab',
                  'Silverado 1500 Limited Double Cab','Silverado 1500 Limited Regular Cab',
                  'Silverado 2500 HD Crew Cab','Silverado 2500 HD Double Cab',
                  'Silverado 2500 HD Regular Cab','Silverado 3500 HD Crew Cab',
                  'Silverado 3500 HD Double Cab','Silverado 3500 HD Regular Cab',
                  'Spark','Suburban','Tahoe','Trailblazer','Traverse','Trax'],
    'chrysler': ['300','Pacifica','Pacifica Hybrid','Voyager'],
    'dodge': ['Charger', 'Challenger', 'Durango'],
    'ferrari': ['296 GTB','812 Competizione','812 Competizione A','812 GTS',
                'F8', 'Portofino', 'SF90', 'Roma'],
    'fiat': ['500X'],
    'ford': ['Bronco', 'Bronco Sport','E-Transit 350 Cargo Van','EcoSport', 'Edge', 
             'Escape','Escape Plug-in Hybrid', 'Expedition','Expedition MAX', 
             'Explorer', 'F150 Lightning', 'F150 Regular Cab','F150 Super Cab',
             'F150 SuperCrew Cab', 'F250 Super Duty Crew Cab','F250 Super Duty Regular Cab',
             'F250 Super Duty Super Cab', 'F350 Super Duty Crew Cab','F350 Super Duty Regular Cab',
             'F350 Super Duty Super Cab', 'F450 Super Duty Crew Cab','F450 Super Duty Regular Cab', 
             'Maverick', 'Mustang','Mustang MACH-E', 'Ranger SuperCab','Ranger SuperCrew', 
             'Transit 150 Cargo Van', 'Transit 150 Crew Van', 'Transit 150 Passenger Van',              
             'Transit 250 Cargo Van', 'Transit 250 Crew Van', 'Transit 350 HD Cargo Van', 'Transit 350 HD Crew Van',
             'Transit 350 Cargo Van', 'Transit 350 Crew Van', 'Transit 350 Passenger Van', 
             'Transit Connect Cargo Van', 'Transit Connect Passenger Wagon'],
    'genesis': ['G70', 'G80','G90', 'GV70','GV80'],
    'gmc': ['Acadia','Canyon Crew Cab','Canyon Extended Cab','HUMMER EV Pickup','Savana 2500 Cargo','Savana 2500 Passenger', 
            'Savana 3500 Cargo','Savana 3500 Passenger','Sierra 1500 Crew Cab', 'Sierra 1500 Double Cab','Sierra 1500 Regular Cab',
            'Sierra 1500 Limited Crew Cab', 'Sierra 1500 Limited Double Cab', 'Sierra 1500 Limited Regular Cab', 
            'Sierra 2500 HD Crew Cab','Sierra 2500 HD Double Cab','Sierra 2500 HD Regular Cab', 'Sierra 3500 HD Crew Cab',
            'Sierra 3500 HD Double Cab','Sierra 3500 HD Regular Cab', 'Yukon', 'Yukon XL', 'Terrain'],
    'honda': ['Accord', 'Accord Hybrid', 'Civic', 'CR-V', 'CR-V Hybrid', 'HR-V', 'Insight', 'Odyssey', 'Passport', 'Pilot', 'Ridgeline'],
    'hyundai': ['Accent', 'Elantra', 'Elantra N' , 'IONIQ5', 'Ioniq Hybrid','Ioniq Plug-in Hybrid','Kona', 'Kona Electric', 'Kona N',
                'Palisade', 'Santa Fe', 'Santa Fe Hybrid', 'Santa Fe Plug-in Hybrid','Sonata', 'Sonata Hybrid', 'Tucson', 'Tucson Hybrid', 
                'Tucson Plug-in Hybrid', 'Venue', 'Veloster', 'Santa Cruz'],
    'infiniti': ['Q50', 'Q60','QX50','QX55','QX60','QX80'],
    'jaguar': ['XF', 'E-PACE','F-PACE','F-TYPE', 'I-PACE'],
    'jeep': ['Cherokee', 'Compass', 'Gladiator', 'Grand Cherokee', 'Grand Cherokee 4xe', 'Grand Cherokee L', 'Grand Wagoneer','Renegade', 
             'Wagoneer','Wrangler','Wrangler Unlimited', 'Wrangler Unlimited 4xe'],
    'kia': ['Cadenza', 'Forte', 'K5', 'K900', 'Niro', 'Rio', 'Seltos', 'Sorento', 'Soul', 'Sportage', 'Stinger', 'Telluride'],
    'lamborghini': ['Aventador', 'Huracan', 'Urus','Gallardo'],
    'land rover': ['LR2','LR4','Defender', 'Discovery', 'Discovery Sport', 'Range Rover', 'Range Rover Evoque', 'Range Rover Sport', 'Range Rover Velar'],
    'lexus': ['ES', 'GS', 'GX', 'IS', 'LS', 'LX', 'NX', 'RC', 'RX', 'UX','CT'],
    'lincoln': ['Aviator', 'Continental', 'Corsair', 'MKS','MKZ','MKT','MKX', 'Nautilus', 'Navigator', 'Navigator L'],
    'lincoln': ['Navigator', 'Aviator', 'Corsair'],
    'lucid': ['Air'],
    'maserati': ['Ghibli', 'GranTurismo','Levante','MC20', 'Quattroporte'],
    'mazda': ['CX-30', 'CX-5', 'CX-9', 'Mazda3', 'Mazda6', 'MX-5 Miata'],
    'mclaren': ['570S', '600LT', '720S', '765LT','GT'],
    'mercedes-benz': ['A-Class', 'C-Class', 'E-Class', 'G-Class', 'GLA', 'GLC', 'GLE', 'GLS', 'S-Class'],
    'mini': ['Clubman', 'Convertible', 'Countryman', 'Hardtop'],
    'mitsubishi': ['Outlander', 'Eclipse Cross', 'Pajero'],
    'nissan': ['370Z', 'Altima', 'Armada', 'Frontier', 'Kicks', 'LEAF', 'Maxima', 'Murano', 'NV Cargo', 'NV Passenger', 'NV200', 'Pathfinder', 'Rogue', 'Rogue Sport', 'Titan', 'Versa'],
    'polestar': ['2', '1', '3'],
    'porsche': ['911', 'Cayenne', 'Macan', 'Panamera', 'Taycan'],
    'ram': ['1500', '2500', '3500'],
    'rivian': ['R1T', 'R1S'],
    'rolls-royce': ['Cullinan', 'Dawn', 'Ghost', 'Phantom', 'Wraith'],
    'subaru': ['Ascent', 'BRZ', 'Crosstrek', 'Forester', 'Impreza', 'Legacy', 'Outback', 'WRX'],
    'tesla': ['Model 3', 'Model S', 'Model X', 'Model Y'],
    'toyota': ['4Runner', 'Avalon', 'C-HR', 'Camry', 'Corolla', 'Highlander', 'Land Cruiser', 'Prius', 'RAV4', 
               'Sequoia', 'Sienna', 'Tacoma', 'Tundra', 'Venza', 'Yaris'],
    'volkswagen': ['Arteon', 'Atlas', 'Golf', 'Jetta', 'Passat', 'Tiguan'],
    'volvo': ['S60', 'S90', 'V60', 'V90', 'XC40', 'XC60', 'XC90'],
}

# %%

from difflib import get_close_matches

title = cars['title']

# Function to extract make from title
def extract_make(title):
    title_lower = title.lower()
    for make in kbb_make:
        if make in title_lower:
            return make
    return None

# Initialize an empty list to store the extracted models
models = []

# Iterate over each row
for index, row in cars.iterrows():
    make = row['manufacturer']
    
    # Check if the make is in the kbb_make dictionary
    if make in kbb_make:
        # Check if the make is in the kbb_models dictionary
        if make in kbb_models:
            # Extract the model based on the make
            title_lower = row['title'].lower()
            model_options = kbb_models[make]
            
            # Try to find an exact match in the title
            model = next((m for m in model_options if m.lower() in title_lower), None)
            
            # If exact match not found, find the closest match
            if model is None:
                closest_matches = get_close_matches(title_lower, model_options)
                if closest_matches:
                    model = closest_matches[0]
                else:
                    # If no close matches, choose the first model
                    model = model_options[0]
            
            models.append(model)
        else:
            models.append(None)
    else:
        models.append(None)

# Add the 'model' column to the DataFrame
cars['model'] = models

# Apply the extraction functions
cars['manufacturer'] = cars['title'].apply(extract_make)

# Print the DataFrame with 'manufacturer' and 'model'
print(cars[['manufacturer', 'model']])

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data = cars, x = 'manufacturer', y = 'price', estimator = np.median, ax = ax).set(title = 'Median List Price by Manufacturer')
plt.xticks(rotation = 45)


# %%
cars.groupby(['manufacturer'])['price'].median().sort_values(ascending = False)

# %%
cars['manufacturer'].value_counts()

# %%
numeric_columns = ['price', 'year', 'odometer','age']
#cars.groupby(['title_status'])[numeric_columns].median()

# %% [markdown]
# ## Modeling

# %% [markdown]
# ### Segmentation

# %%
cars.head()

# %%
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
from difflib import get_close_matches
import matplotlib.pyplot as plt
import seaborn as sns

# Function to scrape current market price from Kelly Blue Book
def get_kbb_price(row):
    base_url = 'https://www.kbb.com/'
    
    # Check if vehicle_make and vehicle_model are not None or float
    if isinstance(row['manufacturer'], str) and isinstance(row['model'], str):
        # Replace spaces with dashes in the manufacturer and model for the URL
        make_url_part = row["manufacturer"].lower().replace(" ", "-")
        model_url_part = row["model"].lower().replace(" ", "-")
        
        search_url = f'{base_url}{make_url_part}/{model_url_part}/{row["year"]}/'
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract relevant information (adjust based on the actual HTML structure)
            # Extract the price information from the HTML code
            #price_field = soup.find('div', {'class': 'nationalBaseDefaultPrice'})
            #kbb_price = price_field['content'] if price_field else None

            # Use regular expression to extract the price information
            pattern = re.compile(r'"nationalBaseDefaultPrice":(\d+),')
            match = pattern.search(response.text)
            
            kbb_price = match.group(1) if match else None

            return kbb_price

            #return kbb_price.text.strip() if kbb_price else None
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        return None


# Use ThreadPoolExecutor to parallelize the scraping process
with ThreadPoolExecutor(max_workers=5) as executor:
    kbb_prices = list(executor.map(get_kbb_price, cars.to_dict(orient='records')))

# Add the kbb_prices to the DataFrame
cars['kbb_price'] = kbb_prices

# Compare the actual market price with the dataset
cars['price_difference'] = cars['price'] - cars['kbb_price'].astype(float)

# Print the results
#print(cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference']])

# Print the results
output_df = cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference']]
print(output_df)

# Save the results to a CSV file
output_csv_filename = 'price_comparison_results.csv'
output_df.to_csv(output_csv_filename, index=False)
print(f'Results have been saved to {output_csv_filename}')


# Visualize the comparison
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(data=cars, x='manufacturer', y='price_difference', estimator=np.median, ax=ax).set(title='Median Price Difference by Manufacturer')
plt.xticks(rotation=45)
plt.show()

# %%
cars['kbb_price'] = pd.to_numeric(cars['kbb_price'], errors='coerce')

# Calculate the percentage difference between the actual price and KBB price
cars['price_difference_percentage'] = ((cars['price'] - cars['kbb_price']) / cars['kbb_price']) * 100

# Set a threshold for percentage difference, beyond which a vehicle is flagged as potentially fraudulent
fraud_threshold = 10  # You can adjust this threshold based on your criteria

# Create a new column 'fraudulent' to flag potentially fraudulent vehicles
cars['fraudulent'] = np.abs(cars['price_difference_percentage']) > fraud_threshold

# Print or analyze the flagged vehicles
fraudulent_vehicles = cars[cars['fraudulent']]
print(fraudulent_vehicles[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference_percentage']])

# %%
'''
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import IsolationForest
#from sklearn.preprocessing import StandardScaler
#from sklearn.metrics import classification_report

#features = ['year', 'odometer']
#target = 'price'
data = cars[features + [target]].copy()

train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

scaler = StandardScaler()
train_data[features] = scaler.fit_transform(train_data[features])
test_data[features] = scaler.transform(test_data[features])

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(train_data[features])

test_data['anomaly_score'] = model.decision_function(test_data[features])

threshold = -0.2

test_data['anomaly'] = test_data['anomaly_score'] < threshold

print(classification_report(test_data[target], ~test_data['anomaly']))
'''



