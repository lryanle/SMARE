# import necessary libraries
import pandas as pd
import numpy as np
import datetime
import re
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, DotProduct, RBF
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor

import car_data


# MARKET PRICE COMPARISION
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
from difflib import get_close_matches


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
    kbb_prices = list(executor.map(get_kbb_price, car_data.cars.to_dict(orient='records')))

# Add the kbb_prices to the DataFrame
car_data.cars['kbb_price'] = kbb_prices

# Drop rows where kbb_price is empty
cars = car_data.cars.dropna(subset=['kbb_price'])

# Compare the actual market price with the dataset using absolute difference
cars['price_difference'] = np.abs(cars['price'] - cars['kbb_price'].astype(float))

# Print the results
#print(cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference']])

# Flag rows with price difference greater than 10000 as fraudulent
cars['fraudulent'] = np.where(cars['price_difference'] > 10000, True, False)

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Split the dataset into features (X) and target variable (y)
X = cars[['manufacturer', 'model', 'year', 'odometer']]
y = cars['fraudulent']

# Convert categorical variables to numerical using one-hot encoding
X_encoded = pd.get_dummies(X, drop_first=True)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

from sklearn.dummy import DummyClassifier

# Create and train the baseline model (predicts the most frequent class)
baseline_model = DummyClassifier(strategy='most_frequent')
baseline_model.fit(X_train, y_train)

# Evaluate the baseline model
baseline_accuracy = baseline_model.score(X_test, y_test)

# Evaluate the RandomForestClassifier model
model_accuracy = model.score(X_test, y_test)

# Compare the performance of the models
performance_comparison = "RandomForestClassifier model outperforms the baseline model." if model_accuracy >= baseline_accuracy else "RandomForestClassifier model does not outperform the baseline model."

from sklearn.ensemble import GradientBoostingClassifier

# Initialize the Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)

# Train the Gradient Boosting model
gb_model.fit(X_train, y_train)

# Make predictions on the test set
gb_predictions = gb_model.predict(X_test)

# Evaluate the Gradient Boosting model
gb_accuracy = accuracy_score(y_test, gb_predictions)

# Define risk levels based on the magnitude of price difference
def categorize_risk(price_difference):
    if price_difference < 5000:
        return 'Low Risk'
    elif price_difference < 10000 and price_difference > 5001:
        return 'Moderate Risk'
    else:
        return 'High Risk'

# Apply the categorize_risk function to create a new column 'risk_level'
cars['risk_level'] = cars['price_difference'].apply(categorize_risk)

# View the DataFrame with the new 'risk_level' column
#print(cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference', 'risk_level']])

# Print the results
output_df = cars[['manufacturer', 'model', 'year', 'price', 'kbb_price', 'price_difference', 'risk_level']]

# Save the results to a CSV file
output_csv_filename = 'price_comparison_results.csv'
output_df.to_csv(output_csv_filename, index=False)
print(f'Results have been saved to {output_csv_filename}')
