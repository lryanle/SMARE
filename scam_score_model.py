import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline  # Importing Pipeline
from sklearn.ensemble import IsolationForest
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Load data
data = pd.read_csv('data-1.csv')

# 1. Feature Selection and Preprocessing
features = data[['source', 'title', 'price', 'location', 'odometer']].copy()

# New Feature: Count of images
image_columns = [col for col in data.columns if col.startswith('images/')]
data['image_count'] = data[image_columns].notna().sum(axis=1)
features['image_count'] = data['image_count']

# Handling missing values in text columns
features[['source', 'title', 'location']].fillna('', inplace=True)

# Convert price and odometer to numerical values
features['price'] = features['price'].replace('[\$,]', '', regex=True)
features['price'] = pd.to_numeric(features['price'], errors='coerce')

# Convert odometer to numerical values
def convert_odometer(odometer_str):
    if pd.isna(odometer_str):
        return None
    number_part = re.findall(r'\d+', odometer_str)
    if number_part:
        number = int(number_part[0])
        if 'k' in odometer_str.lower():
            return number * 1000  # Convert 'k' to thousands
        return number
    return None

features['odometer'] = features['odometer'].apply(convert_odometer)

# Text preprocessing for 'title'
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = word_tokenize(text)
    text = [word for word in text if word.isalpha()]  # Remove non-alphabetic tokens
    text = [word for word in text if not word in stop_words]  # Remove stopwords
    return ' '.join(text)

features['title'] = features['title'].apply(clean_text)

# Preprocessing Pipeline
num_features = ['price', 'odometer', 'image_count']
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

# 2. Unsupervised Anomaly Detection
# Applying Isolation Forest for anomaly detection
model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
features_preprocessed = preprocessor.fit_transform(features)
model.fit(features_preprocessed)

# 3. Score the listings and save results
scores = model.decision_function(features_preprocessed)

# Saving preprocessed, cleaned data as a new dataframe for better visibility.
# Does not include feature scaling or one-hot encoding. 
model_data = features.copy()
model_data['anomaly_score'] = scores

# Add 'has_anomaly' column: 1 for scores <= 0.05 (potential scam), 0 otherwise
model_data['has_anomaly'] = (scores <= 0.05).astype(int)

# Saving this new DataFrame
model_data.to_csv('model_data_with_anomalies.csv', index=False)

# Count and print the number of listings with an anomaly score of .05 or less
num_anomalous_listings = (scores <= .05).sum()
print(f"Number of listings with anomaly score of 0.05 or less: {num_anomalous_listings}")

scores_df = pd.DataFrame({
    'listing_link': data['_id'],
    'anomaly_score': scores
})

# Save the scores and links to a CSV file
scores_df.to_csv('scores_and_links.csv', index=False)