import pandas as pd
import re
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest

# Load data
data = pd.read_csv('data-1.csv')  # Replace with your file path

# Define luxury brands and their average prices
luxury_brands = ['Mercedes-Benz', 'BMW', 'Audi', 'Lexus', 'Porsche', 'Tesla', 
                 'Jaguar', 'Land Rover', 'Maserati', 'Ferrari', 'Lamborghini', 
                 'Bentley', 'Rolls-Royce']
average_prices = {'Mercedes-Benz': 38000, 'BMW': 32000, 'Audi': 30000, 'Lexus': 30000, 'Porsche': 72000, 'Tesla': 34000, 
                  'Jaguar': 28500, 'Land Rover': 43000, 'Maserati': 43800, 'Ferrari': 192000, 'Lamborghini': 227000, 
                  'Bentley': 122600, 'Rolls-Royce': 173800}

# Function to extract make from the title
def extract_make(title):
    for brand in luxury_brands:
        if brand.lower() in title.lower():
            return brand
    return None

# Function to check if the title contains any luxury brand
def is_luxury(title):
    make = extract_make(title)
    return 1 if make in luxury_brands else 0

# Apply the function to the 'title' column and extract make
data['is_luxury'] = data['title'].apply(is_luxury)
data['make'] = data['title'].apply(extract_make)

data['price'] = data['price'].replace('Free', '$0')
# Convert price to a numerical value
data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)

# Calculate price discrepancy and scale the 'is_luxury' feature
def calculate_discrepancy(row):
    make = row['make']
    if make and make in average_prices:
        avg_price = average_prices[make]
        return abs(row['price'] - avg_price) / avg_price
    return 0

data['price_discrepancy'] = data.apply(calculate_discrepancy, axis=1)
data['is_luxury_scaled'] = data['is_luxury'] / (1.0000001 - data['price_discrepancy'])

# New Feature: Count of images
data['image_count'] = data.notna().sum(axis=1) - 9

# Feature Selection and Preprocessing
features = data[['source', 'title', 'location', 'price', 'odometer', 'image_count', 'is_luxury_scaled']].copy()

# Handling missing values in text columns
features[['source', 'location']].fillna('', inplace=True)

# Convert odometer to numerical values
features['odometer'] = features['odometer'].apply(lambda x: int(re.findall(r'\d+', x)[0]) if pd.notna(x) else None)

# Preprocessing Pipeline
num_features = ['price', 'odometer', 'image_count', 'is_luxury_scaled']
cat_features = ['source', 'location']

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_pipeline, num_features),
        ('cat', OneHotEncoder(), cat_features)
    ])

# Retrain Isolation Forest Model
model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
features_preprocessed = preprocessor.fit_transform(features)
model.fit(features_preprocessed)

# Score the listings and save results
scores = model.decision_function(features_preprocessed)

# Add 'has_anomaly' column
features['anomaly_score'] = scores
features['has_anomaly'] = (scores <= 0.05).astype(int)

# Save the new DataFrame
features.to_csv('model_data_with_anomalies_and_luxury.csv', index=False)

# Count listings with anomaly score of 0.05 or less
num_anomalous_listings = (scores <= 0.05).sum()
print(f"Number of listings with anomaly score of 0.05 or less: {num_anomalous_listings}")