# import necessary libraries
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import car_data

# MARKET PRICE COMPARISION
cars_df = car_data.cars

# Function to scrape current market price from Kelly Blue Book
def get_kbb_price(row):
    base_url = 'https://www.kbb.com/'
    
    # Check if vehicle_make and vehicle_model are not None or float
    if isinstance(row['manufacturer'], str) and isinstance(row['model'], str):
        # Replace spaces with dashes in the manufacturer and model for the URL
        make_url_part = row["manufacturer"].lower().replace(" ", "-")
        model_url_part = row["model"].lower().replace(" ", "-")
        
        search_url = f'{base_url}{make_url_part}/{model_url_part}/{row["year"]}/'
        #print(search_url)
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
    kbb_prices = list(executor.map(get_kbb_price, cars_df.to_dict(orient='records')))

cars_df['kbb_price'] = kbb_prices

# Convert 'price' and 'kbb_price' columns to numerical types
cars_df['price'] = pd.to_numeric(cars_df['price'], errors='coerce')
cars_df['kbb_price'] = pd.to_numeric(cars_df['kbb_price'], errors='coerce')
#print(cars_df.columns)

# Drop rows where 'price' or 'kbb_price' is NaN after conversion
cars_df = cars_df.dropna(subset=['price', 'kbb_price'])

# Calculate price difference
cars_df.loc[:,'price_difference'] = np.abs(cars_df['price'] - cars_df['kbb_price'].astype(float))

# Function to calculate reasonable price difference (rd_kbb)
def calculate_reasonable_difference(kbb_price):
    a = 20000  # Initial value at x = 0
    b = (1.06) ** (1/10000)  # Base of the exponential function
    rd_kbb = a * (b ** (1.19*kbb_price))- 20000
    return rd_kbb

# Function to calculate risk score (y)
def calculate_risk_score(listed_price, kbb_price):
    # Calculate absolute difference between listed price and KBB price
    delta_p = np.abs(listed_price - kbb_price)
    
    # Calculate reasonable price difference
    rd_kbb = calculate_reasonable_difference(kbb_price)

    # Calculate scaled difference (x)
    x = delta_p / rd_kbb

    # Calculate risk score (y) using logistic or logarithmic regression function
    y = 0.26 * x**2 + 0.07 * x
    y = np.clip(y, 0, 1)
    
    return y

# Calculate risk score
cars_df.loc[:,'risk_score'] = cars_df.apply(lambda row: calculate_risk_score(row['price'], row['kbb_price']), axis=1)

# Print the results
output_df = cars_df[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference','risk_score']]

# Save the results to a CSV file
output_csv_filename = 'price_comparison_results.csv'
output_df.to_csv(output_csv_filename, index=False)
print(f'Results have been saved to {output_csv_filename}')
