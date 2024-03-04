# import necessary libraries
import pandas as pd
import car_data

#VEHICLE FREQUENCY MODEL
# Function to analyze frequency of vehicle models
def analyze_frequency(vehicle_data):
    model_frequency = vehicle_data['model'].value_counts()
    return model_frequency

# Function to assess risk associated with vehicles based on frequency
def assess_risk(model_frequency, threshold=10):
    # Define a threshold for significant frequency
    # Vehicles with frequency above this threshold are considered high risk
    high_risk_models = model_frequency[model_frequency > threshold].index.tolist()
    return high_risk_models

# Analyze frequency of vehicle models
model_frequency = analyze_frequency(car_data.cars)

# Assess risk associated with vehicles based on frequency
high_risk_models = assess_risk(model_frequency)

# Add a column to indicate if the model is high risk
car_data.cars['high_risk'] = car_data.cars['model'].apply(lambda x: x in high_risk_models)

# Save high-risk models to CSV
#high_risk_models_df = pd.DataFrame(high_risk_models, columns=['High Risk Models'])
#high_risk_models_df.to_csv('high_risk_models.csv', index=False)

# Save high-risk vehicles data to CSV
#high_risk_cars_df = cars[cars['high_risk']]
#high_risk_cars_df.to_csv('high_risk_cars.csv', index=False)


# Function to create better visuals for frequency analysis
def visualize_frequency(model_frequency, threshold=10):
    # Plotting frequency of vehicle models
    model_frequency_df = pd.DataFrame(model_frequency, columns=['Model Frequency'])
    model_frequency_df.to_csv('model_frequency.csv')

# Visualize frequency of vehicle models
visualize_frequency(model_frequency, threshold=10)

# Function to create better visuals for risk assessment
def visualize_risk(high_risk_models):
    # Plotting high-risk models
    high_risk_models_df = pd.DataFrame(high_risk_models, columns=['High Risk Models'])
    high_risk_models_df.to_csv('high_risk_models.csv', index=False)


# Visualize high-risk vehicle models
visualize_risk(high_risk_models)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Define Target Variable
target_variable = 'high_risk'

# Step 2: Feature Selection
# Select relevant features
#features = ['age', 'odometer', 'manufacturer', 'model']  # Add more features as needed
# Assuming all columns except 'high_risk' are features
features = [col for col in car_data.cars.columns if col != target_variable]

# Make a copy of the DataFrame
cars_encoded = car_data.cars.copy()

# Example: Convert categorical variables to numerical using one-hot encoding
cars_encoded = pd.get_dummies(cars_encoded, columns=[col for col in cars_encoded.columns if col not in [target_variable]], drop_first=True)

# Step 5: Split Data
X = cars_encoded.drop(columns=[target_variable])
y = cars_encoded[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 7: Model Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_report_str = classification_report(y_test, y_pred, output_dict=True)

# Save accuracy to CSV
accuracy_df = pd.DataFrame([accuracy], columns=['Accuracy'])
accuracy_df.to_csv('accuracy.csv', index=False)

# Save classification report to CSV
classification_report_df = pd.DataFrame(classification_report_str).transpose()
classification_report_df.to_csv('classification_report.csv')

from sklearn.dummy import DummyClassifier

# Create and train the baseline model (predicts the most frequent class)
baseline_model = DummyClassifier(strategy='most_frequent')
baseline_model.fit(X_train, y_train)

# Evaluate the baseline model
baseline_accuracy = baseline_model.score(X_test, y_test)
baseline_accuracy_df = pd.DataFrame([baseline_accuracy], columns=['Baseline Model Accuracy'])
baseline_accuracy_df.to_csv('baseline_accuracy.csv', index=False)

# Evaluate the RandomForestClassifier model
model_accuracy = model.score(X_test, y_test)
model_accuracy_df = pd.DataFrame([model_accuracy], columns=['RandomForestClassifier Model Accuracy'])
model_accuracy_df.to_csv('model_accuracy.csv', index=False)

# Compare the performance of the models
performance_comparison = "RandomForestClassifier model outperforms the baseline model." if model_accuracy >= baseline_accuracy else "RandomForestClassifier model does not outperform the baseline model."
performance_comparison_df = pd.DataFrame([performance_comparison], columns=['Performance Comparison'])
performance_comparison_df.to_csv('performance_comparison.csv', index=False)

# Create a new column 'model_frequency' to represent the frequency of each model
car_data.cars['model_frequency'] = car_data.cars['model'].map(car_data.cars['model'].value_counts())

# Iterate through each row in the DataFrame
for index, row in car_data.cars.iterrows():
    manufacturer = row['manufacturer']
    model = row['model']
    frequency = row['model_frequency']

# Extract the first four letters of each model
car_data.cars['model_short'] = car_data.cars['model'].str[:4]

# Save cars DataFrame with new columns to CSV
car_data.cars.to_csv('cars_with_model_frequency.csv', index=False)


