import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import make_pipeline

# Load the dataset
data = pd.read_csv("model_data_with_anomalies.csv")  # Replace with your file path

# Define a list of luxury car brands
luxury_brands = [
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Lexus",
    "Porsche",
    "Tesla",
    "Jaguar",
    "Land Rover",
    "Maserati",
    "Ferrari",
    "Lamborghini",
    "Bentley",
    "Rolls-Royce",
]


# Function to check if the title contains any luxury brand
def is_luxury(title):
    for brand in luxury_brands:
        if brand.lower() in title.lower():
            return 1
    return 0


# Apply the function to the 'title' column
data["is_luxury"] = data["title"].apply(is_luxury)

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(
    data["title"], data["is_luxury"], test_size=0.3, random_state=42
)

# Creating a pipeline with TF-IDF Vectorizer, SMOTE, and RandomForestClassifier
pipeline = make_pipeline(
    TfidfVectorizer(), SMOTE(random_state=42), RandomForestClassifier(random_state=42)
)

# Training the model
pipeline.fit(X_train, y_train)

# Predictions
y_pred = pipeline.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(report)
