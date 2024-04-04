import json
import numpy as np
from difflib import SequenceMatcher
from ..utilities import logger
import requests
from bs4 import BeautifulSoup

# Initialize logger
logger = logger.SmareLogger()

# Load KBB prices from the JSON file into memory
kbb_price_file = "/var/task/src/models/kbb_prices.json"
with open(kbb_price_file, "r") as kbb_file:
    kbb_prices = json.load(kbb_file)

# Function to scrape KBB price
def scrape_kbb_price(make, model, year):
    try:
        make_url_part = make.lower().replace(" ", "-")
        model_url_part = model.lower().replace(" ", "-")
        search_url = f'https://www.kbb.com/{make_url_part}/{model_url_part}/{year}/'
        response = requests.get(search_url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and '"nationalBaseDefaultPrice"' in script.string:
                start_index = script.string.find('"nationalBaseDefaultPrice"') + len('"nationalBaseDefaultPrice"') + 1
                end_index = script.string.find(',', start_index)
                kbb_price = script.string[start_index:end_index]
                return kbb_price
        logger.error(f"Failed to extract price for {make} {model} {year}.")
        return None
    except Exception as e:
        logger.error(f"An error occurred while scraping {make} {model} {year}: {e}")
        return None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_similar_listing(car_data):
    year = car_data['year']
    make = car_data['make']
    model = car_data['model']
    input_string = f"{year} {make} {model}"
    max_similarity = 0
    for key in kbb_prices.keys():
        entry_make, entry_model, entry_year = key.split()
        similarity = similar(input_string.lower(), f"{entry_year} {entry_make} {entry_model}".lower())
        try:
            if similarity > max_similarity and abs(year - int(entry_year)) <= 5:
                max_similarity = similarity
                kbb_price = kbb_prices[key]
                return kbb_price
        except ValueError:
                pass
    return None


def m3_riskscores(car_listings):
    risk_scores = []
    if not isinstance(car_listings, list):
        car_listings = [car_listings] 
        logger.warning("Model 3: Input is not a list. Converting to a list.")
    if len(car_listings) == 0:
        logger.error("Model 3: Input list is empty.")
        return []
        
    for k, data in enumerate(car_listings):
        try:
            year = data.get('year')
            price = data.get('price')
            make = data.get('make')
            model = data.get('model')

            kbb_price_key = f"{make} {model} {year}"
            kbb_price = kbb_prices.get(kbb_price_key)

            if kbb_price is None:
                kbb_price = scrape_kbb_price(make, model, year)
                if kbb_price is None:
                    kbb_price = find_similar_listing(data)
                    if kbb_price is None:
                        logger.error(f"Model 3: KBB price not found for {make} {model} {year}")
                        risk_scores.append(-1)
                        continue    
            try:               
                kbb_price = float(kbb_price)
                price = float(price)
                a = 20000  
                b = (1.06) ** (1 / 10000)  
                rd_kbb = a * (b ** (1.19 * kbb_price)) - a
                if price > kbb_price:
                    risk_score = 0.0
                else:
                    delta_p = np.abs(price - kbb_price)
                    x = delta_p / rd_kbb
                    y = 0.26 * x ** 2 + 0.07 * x
                    y = max(0, min(1, y))  
                    risk_score = y
                risk_scores.append(risk_score)
            except ValueError:
                logger.error(f"Model 3: Error: Could not parse price data for {make} {model} {year}")
                risk_scores.append(-1)
        except Exception as e:
            logger.warning(f"Error in M3_Model3: {e}")
            risk_scores.append(-1)
            continue
    # Check input and output array sizes after processing all listings
    if len(car_listings) != len(risk_scores):
        logger.error("Model 3: Input and output array sizes do not match.")
        return [-1] * len(car_listings)
    return risk_scores
