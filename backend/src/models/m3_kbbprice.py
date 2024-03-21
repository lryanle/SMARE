import json
import re
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
import requests

from ..utilities import logger

# Initialize logger
logger = logger.SmareLogger()


def m3_riskscores(car_listings):
    try:
        logger.info("Starting M3 model for calculating risk scores...")
       
        # Ensure the input is a list even if it's a single object
        if not isinstance(car_listings, list):
            car_listings = [car_listings]  # Convert single object input to list
            logger.error("Input is not a list. Converting to a list.")

        if len(car_listings) == 0:
            logger.warning("Input list is empty.")
            return []
        
        risk_scores = []

        for data in car_listings:
            # Extract relevant data
            year = data.get('year')
            price = data.get('price')
            make = data.get('make')
            model = data.get('model')

            # MARKET PRICE COMPARISON
            base_url = "https://www.kbb.com/"

            # Check if make and model are strings
            if not all(isinstance(val, str) for val in [make, model]):
                logger.warning("Make or model is not a string!")
                continue

            # Replace spaces with dashes in the make and model for the URL
            make_url_part = make.lower().replace(" ", "-")
            model_url_part = model.lower().replace(" ", "-")

            search_url = f'{base_url}{make_url_part}/{model_url_part}/{year}/'

            try:
                response = requests.get(search_url)
                pattern = re.compile(r'"nationalBaseDefaultPrice":(\d+),')
                match = pattern.search(response.text)
                kbb_price = match.group(1) if match else None

                if kbb_price is None:
                    logger.warning(f"KBB price not found for {make} {model} {year}")
                    continue

                kbb_price = float(kbb_price)
                price = float(price)

                # Calculate price difference
                price_difference = np.abs(price - kbb_price)

                # Calculate reasonable price difference
                a = 20000  # Initial value at x = 0
                b = (1.06) ** (1 / 10000)  # Base of the exponential function
                rd_kbb = a * (b ** (1.19 * kbb_price)) - 20000

                # Calculate risk score
                if price > kbb_price:
                    risk_score = 0.01
                else:
                    delta_p = np.abs(price - kbb_price)
                    x = delta_p / rd_kbb
                    y = 0.26 * x ** 2 + 0.07 * x
                    y = max(0, min(1, y))  # Ensure the risk score is between 0 and 1
                    risk_score = y

                risk_scores.append(risk_score)
                logger.info(f"Risk score calculated for {make} {model} {year}: {risk_score}")

            except Exception as e:
                logger.error(f"Error processing {make} {model} {year}: {e}")

        return risk_scores
    
    except Exception as e:
        logger.error(f"Error in M3 model: {e}")
        return None

def test_m3():
    try:
        # Load data from the JSON file-- I used the cars.json just for testing purposes
        with open("cars.json", "r") as file:
            car_listings = json.load(file)
        # Call the m3_riskscores function
        risk_scores = m3_riskscores(car_listings)
        if risk_scores is not None:
            # Print the risk scores
            logger.info("Risk Scores:")
            logger.info(risk_scores)
        else:
            logger.info("Error occurred while calculating risk scores.")
    except Exception as e:
        logger.error(f"Error in M3 model tester: {e}")

# Call the tester function
test_m3()
