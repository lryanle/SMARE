import pandas as pd
import numpy as np
import re
import seaborn as sns
import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
#from pymongo import MongoClient

# Load sentiment analysis model from transformers library
sentiment_analysis_model = pipeline("sentiment-analysis")

# Function to load the dataset from MongoDB
def load_data(database_name, collection_name):
    # Connect to MongoDB
    client = MongoClient('mongodb://yeabgezz%40gmail.com:Gezahgne204012@localhost:27017/')  # Replace with your MongoDB connection string
    db = client[database_name]
    collection = db[collection_name]

    # Fetch data from MongoDB and convert to DataFrame
    cursor = collection.find()
    cars = pd.DataFrame(list(cursor))

    # Close MongoDB connection
    client.close()

    return cars

# Function to drop unnecessary columns from the dataset
def drop_unnecessary_columns(data):
    unnecessary_columns = ['_id', 'link', 'images/23', ...]  # List of unnecessary columns
    data = data.drop(columns=unnecessary_columns)
    return data

# Function to clean the dataset by handling missing values and converting data types
def clean_data(data):
    data = data.dropna()
    data['odometer'] = data['odometer'].apply(lambda x: int(re.search(r'\d+', str(x)).group(0)) if re.search(r'\d+', str(x)) else None)
    data['year'] = data['title'].str.extract(r'(\d{4})')
    data['year'].fillna(-1, inplace=True)
    data = data.astype({'year':'int', 'odometer':'int'})
    data['age'] = datetime.date.today().year - data['year']
    return data

# Function to filter the dataset based on specified criteria
def filter_data(data):
    data = data[data['year'] >= 2005]
    data = data[data['odometer'] <= 300]
    data['price'] = pd.to_numeric(data['price'].replace('[\$,]', '', regex=True), errors='coerce')
    data['price'].fillna(-1, inplace=True)
    data['price'] = data['price'].astype(int)
    data = data[data['price'] <= 100000]
    data = data[data['price'] >= 1000]
    return data

# Function to extract manufacturer information from the 'title' column
def extract_manufacturer(data):
    data['manufacturer'] = data['title'].str.extract(r'(\b\w+)(?=\s\d{4})')
    return data

# Function to visualize the median list price by manufacturer
def visualize_price_by_manufacturer(data):
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(data=data, x='manufacturer', y='price', estimator=np.median, ax=ax).set(title='Median List Price by Manufacturer')
    plt.xticks(rotation=45)
    plt.show()

# Function to preprocess data for machine learning tasks
def preprocess_data(data):
    features = ['year', 'odometer']
    target = 'price'
    train_data, test_data = train_test_split(data[features + [target]], test_size=0.2, random_state=42)
    scaler = StandardScaler()
    train_data[features] = scaler.fit_transform(train_data[features])
    test_data[features] = scaler.transform(test_data[features])
    return train_data, test_data

# Function to detect anomalies in the dataset using Isolation Forest
def detect_anomalies(train_data, test_data):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(train_data[['year', 'odometer']])
    test_data['anomaly_score'] = model.decision_function(test_data[['year', 'odometer']])
    threshold = -0.2
    test_data['anomaly'] = test_data['anomaly_score'] < threshold
    return test_data

# Function to extract the car model from the 'title' column
def extract_car_model(title):
    model_pattern = re.compile(r'\d{4}\s([a-zA-Z0-9\s]+)')
    match = model_pattern.search(title)
    return match.group(1).strip() if match else None

# Function to scrape Kelly Blue Book for current market price
def get_kbb_price(vehicle_make, vehicle_model, vehicle_year):
    base_url = 'https://www.kbb.com/'
    if isinstance(vehicle_make, str) and isinstance(vehicle_model, str):
        search_url = f'{base_url}{vehicle_make.lower()}/{vehicle_model.lower()}/{vehicle_year}/'
        try:
            response = requests.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            kbb_price = soup.find('span', {'class': 'css-x7sd52-Price'})
            return kbb_price.text.strip() if kbb_price else None
        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        return None

# Function to analyze sentiment of a post based on fields such as title and post body
def analyze_sentiment(title, body):
    # Combine title and body for sentiment analysis
    text_to_analyze = f"{title} {body}"
    # Use GPT model for sentiment analysis
    sentiment_result = sentiment_analysis_model(text_to_analyze)
    return sentiment_result[0]

# Function to compare actual prices with prices from Kelly Blue Book
def compare_prices_with_kbb(data):
    data['model'] = data['title'].apply(extract_car_model)
    data['kbb_price'] = data.apply(lambda row: get_kbb_price(row['manufacturer'], row['model'], row['year']), axis=1)
    data['price_difference'] = data['price'] - data['kbb_price'].astype(float)
    return data[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference', 'sentiment']]

# Main Script
mongodb_database = 'your_database_name'
mongodb_collection = 'your_collection_name'

cars_data = load_data(mongodb_database, mongodb_collection)
cars_data = drop_unnecessary_columns(cars_data)
cars_data = clean_data(cars_data)
cars_data = filter_data(cars_data)
cars_data = extract_manufacturer(cars_data)
visualize_price_by_manufacturer(cars_data)

# Analyze sentiment for each post and add sentiment column to the DataFrame
cars_data['sentiment'] = cars_data.apply(lambda row: analyze_sentiment(row['title'], row.get('body', '')), axis=1)

# Display a few rows of the DataFrame including the 'sentiment' column
print(cars_data[['title', 'body', 'sentiment']].head())

train_data, test_data = preprocess_data(cars_data)
test_data = detect_anomalies(train_data, test_data)

result_comparison = compare_prices_with_kbb(cars_data)
print(result_comparison)
