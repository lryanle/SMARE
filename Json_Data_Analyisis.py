import json
import pandas as pd
import difflib
import re
import datetime
import requests
from bs4 import BeautifulSoup

# Function to read a list of names from a file
def read_names_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            names = [line.strip() for line in file]
        return names
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

# Function to calculate similarity ratio between two strings
def similarity_ratio(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()

# Function to extract car details from the title
def extract_car_details(title):
    details_pattern = re.compile(r'(\d{4})\s([a-zA-Z0-9\s]+)')
    match = details_pattern.search(title)
    return match.groups() if match else (None, None)

# Function to extract car make from the title (assumes make is the first word)
def extract_car_make(title, car_manufacturers):
    words = title.split()
    if words:
        for word in words:
            # Check if the word is similar to any of the car manufacturers
            ratios = [similarity_ratio(word.lower(), manufacturer.lower()) for manufacturer in car_manufacturers]
            max_ratio = max(ratios)
            if max_ratio > 0.8:
                return car_manufacturers[ratios.index(max_ratio)].strip()
        return 'N/A'  # If no match is found, return 'N/A'
    return None

# Function to extract car year from the title
def extract_car_year(title):
    # Check if the title contains a range of years (e.g., 2000 - current year)
    range_pattern = re.compile(r'(\d{4})\s*-\s*(\d{4})')
    match = range_pattern.search(title)
    if match:
        start_year, end_year = match.groups()
        current_year = datetime.datetime.now().year
        # Return the end year if it's the current year or later, otherwise, return the start year
        return end_year if int(end_year) >= current_year else start_year
    else:
        details_pattern = re.compile(r'(\d{4})\s([a-zA-Z0-9\s]+)')
        match = details_pattern.search(title)
        return match.group(1) if match else 'N/A'

# Function to check if a word in the title is a car model
def is_car_model(word):
    return word.lower() in car_models

# Function to fill in the car_models column based on car_models.txt
def fill_car_models(title):
    words = title.split()

    for word in words:
        # Check if the word is similar to any of the car models
        ratios = [similarity_ratio(word.lower(), model.lower()) for model in car_models]
        max_ratio = max(ratios)

        if max_ratio > 0.8:
            return car_models[ratios.index(max_ratio)].strip()

    return 'N/A'

# Function to scrape KKB for car price
def scrape_kkb_price(make, model, year):
    # Construct the search URL for KKB
    search_url = f'https://www.kbb.com/{make.lower()}/{model.lower()}/{year}/'
    
    # Make a request to the KKB website
    response = requests.get(search_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the price element from the HTML
        price_element = soup.find('span', class_='js-vehicle-base-price')

        # Check if the price element is found
        if price_element:
            return price_element.get_text(strip=True)
        else:
            return 'N/A'  # Return 'N/A' if the price element is not found
    else:
        print(f"Failed to fetch data from KKB for {make} {model} {year}")
        return 'N/A'

# Opening JSON file
with open('data.json') as f:
    data = json.load(f)

# Read car manufacturers and models from files
car_manufacturers = read_names_from_file('car_manufacturers.txt')
car_models = read_names_from_file('car_models.txt')

# Create a DataFrame to organize the data
output_data = []

for item in data:
    title = item.get('title', 'N/A')
    car_manufacturer = extract_car_make(title, car_manufacturers)
    car_models_column = fill_car_models(title)
    car_year = extract_car_year(title)

    # Scrape KKB for car price
    car_price = scrape_kkb_price(car_manufacturer, car_models_column, car_year)

    output_data.append({
        'Title': title,
        'Car_Manufacturer': car_manufacturer,
        'Year': car_year,
        'Car_Models': car_models_column,
        'Price': item['price'],
        'KKB_Price': car_price,
        'Location': item['location'],
        'Odometer': item['odometer'],
        'Link': item['link'],
    })

# Creating DataFrame
df = pd.DataFrame(output_data)

# Writing the DataFrame to a CSV file with specified formatting
csv_file_path = 'output.csv'
df.to_csv(csv_file_path, index=False, float_format='%20.2f', na_rep='N/A', columns=['Title', 'Car_Manufacturer', 'Year', 'Car_Models', 'Price', 'KKB_Price', 'Location', 'Odometer', 'Link'])

print(f"Selected items written to {csv_file_path}")
