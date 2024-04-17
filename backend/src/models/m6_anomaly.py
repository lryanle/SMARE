import os

import joblib
import pandas as pd

from ..utilities import logger

logger = logger.SmareLogger()

# Define luxury brands and their average prices
luxury_brands = ['Mercedes-Benz', 'BMW', 'Audi', 'Lexus', 'Porsche', 'Tesla',
                 'Jaguar', 'Land Rover', 'Maserati', 'Ferrari', 'Lamborghini',
                 'Bentley', 'Rolls-Royce']
average_prices = {'Mercedes-Benz': 38000, 'BMW': 32000, 'Audi': 30000, 'Lexus': 30000, 'Porsche': 72000, 'Tesla': 34000,
                  'Jaguar': 28500, 'Land Rover': 43000, 'Maserati': 43800, 'Ferrari': 192000, 'Lamborghini': 227000,
                  'Bentley': 122600, 'Rolls-Royce': 173800}

# Functions for feature engineering
def extract_make(title):
    for brand in luxury_brands:
        if brand.lower() in title.lower():
            return brand
    return None

def is_luxury(title):
    make = extract_make(title)
    return 1 if make in luxury_brands else 0

def calculate_discrepancy(row):
    make = row['make']
    if make and make in average_prices:
        avg_price = average_prices[make]
        return abs(row['price'] - avg_price) / avg_price
    return 0

# Function to preprocess a single listing
def preprocess_listing(listing):
    title = listing['title'].replace('%20', ' ')
    price = listing['price']
    source = listing['source']
    location = ''  # Assuming location is not provided
    odometer = listing['odometer'] if 'odometer' in listing else None
    image_count = len(listing['images']) if 'images' in listing else 0

    is_luxury_val = is_luxury(title)
    make = extract_make(title)
    price_discrepancy = calculate_discrepancy({'make': make, 'price': price})
    is_luxury_scaled = is_luxury_val / (1.0000001 - price_discrepancy)

    # Create a DataFrame with the features
    features = pd.DataFrame([{
        'source': source, 'title': title, 'location': location,
        'price': price, 'odometer': odometer, 'image_count': image_count,
        'is_luxury_scaled': is_luxury_scaled
    }])

    return features

# Load the model and preprocessor
try:
    model_path = './src/models/isolation_forest_model.pkl'
    preprocessor_path = './src/models/preprocessor.pkl'

    # Log the current working directory and the absolute path of the files
    cwd = os.getcwd()
    logger.info(f"Current working directory: {cwd}")
    logger.info(f"Attempting to load model from: {os.path.join(cwd, model_path)}")
    logger.info(f"Attempting to load preprocessor from: {os.path.join(cwd, preprocessor_path)}")

    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    logger.success("Model and preprocessor successfully loaded.")
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise
except Exception as e:
    logger.error(f"Failed to load model or preprocessor: {e}")
    raise

# Function to predict anomalies on new listings
def m6_labels(listings):
    predictions = []
    for k, listing in enumerate(listings):
        try:
            preprocessed_listing = preprocess_listing(listing)
            features_preprocessed = preprocessor.transform(preprocessed_listing)
            score = model.decision_function(features_preprocessed)
            prediction = 1 if score <= 0.05 else 0
            predictions.append(prediction)
            logger.debug(f"Processed listing {k + 1}/{len(listings)}. Prediction: {prediction}")
        except Exception as e:
            logger.warning(f"Error processing listing {k + 1}: {e}")
            predictions.append(-1)
    return predictions
