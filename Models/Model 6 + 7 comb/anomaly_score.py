import pandas as pd
import joblib

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
    odometer = listing['attributes']['odometer'] if 'odometer' in listing['attributes'] else None
    image_count = len(listing['images'])

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
model = joblib.load('isolation_forest_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# Function to predict anomalies on new listings
def predict_listings(listings):
    predictions = []
    for listing in listings:
        preprocessed_listing = preprocess_listing(listing)
        features_preprocessed = preprocessor.transform(preprocessed_listing)
        score = model.decision_function(features_preprocessed)
        prediction = 1 if score <= 0.05 else 0
        predictions.append(prediction)
    return predictions

import json

# Function to load JSON data
def load_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Load your JSON file
filename = 'listings.json'
listings = load_json(filename)

# Assuming predict_listings function is already defined as per previous script
predictions = predict_listings(listings)

# Display or process the predictions
for listing, prediction in zip(listings, predictions):
    print(f"Listing ID: {listing['_id']} - Anomaly Prediction: {'Anomaly' if prediction == 1 else 'Normal'}")


