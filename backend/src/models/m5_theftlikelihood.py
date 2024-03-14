# import necessary libraries
import backend.src.models.MOVETOCLEAN_car_data as MOVETOCLEAN_car_data
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# THEFT LIKELIHOOD MODEL

# Step 1: Load the datasets
car_df = MOVETOCLEAN_car_data.cars
car_df["make_model"] = car_df["manufacturer"] + " " + car_df["model"]

# Load the dataset containing the Top 10 Most Frequently Stolen Vehicles
top10theft = {
    "Rank": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Model": [
        "Chevrolet Full Size Pick-up",
        "Ford Full Size Pick-up",
        "Honda Civic",
        "Honda Accord",
        "Hyundai Sonata",
        "Hyundai Elantra",
        "Kia Optima",
        "Toyota Camry",
        "GMC Full Size Pick-up",
        "Honda CR-V",
    ],
    "Thefts": [
        49.903,
        48.175,
        27.113,
        27.089,
        21.707,
        19.602,
        18.221,
        17.094,
        16.622,
        13.832,
    ],
    "year": [2004, 2006, 2000, 1997, 2013, 2017, 2015, 2021, 2005, 2001],
}

top10theft = pd.DataFrame(top10theft)


# Function to calculate similarity between strings using fuzzywuzzy
def calculate_similarity(str1, str2):
    return fuzz.token_sort_ratio(str1, str2)


# Function to compare models and years and assign theft occurrences
def assign_theft_occurrences(row):
    for index, theft_row in top10theft.iterrows():
        # Check if model and year are similar
        similarity = calculate_similarity(row["make_model"], theft_row["Model"])
        if similarity >= 80 and abs(row["year"] - theft_row["year"]) <= 5:
            return theft_row["Thefts"]
    # If vehicle not in top 10 list, assign a reasonable number
    return 1000


# Apply the function to assign theft occurrences
car_df["theft_occurrences"] = car_df.apply(assign_theft_occurrences, axis=1)

# Step 2: Preprocess the data (if needed)
# Drop columns that are not needed for modeling
car_df = car_df.drop(
    columns=[
        "source",
        "title",
        "location",
        "kbb_price",
        "price_difference",
        "fraudulent",
        "risk_level",
        "model_frequency",
        "model_short",
        "high_risk",
    ]
)

# One-hot encode categorical variables if needed
car_df = pd.get_dummies(car_df, columns=["manufacturer", "model"])

# Step 3: Split the data into features and target variable
X = car_df.drop(["theft_occurrences", "make_model"], axis=1)
y = car_df["theft_occurrences"]

# Print unique theft_occurrences values and their corresponding make_model and thefts
unique_theft_occurrences = car_df["theft_occurrences"].unique()
for theft_occurrence in unique_theft_occurrences:
    print(f"Theft Occurrence: {theft_occurrence}")
    print("Make Model and Thefts:")
    matched_make_models = car_df.loc[
        car_df["theft_occurrences"] == theft_occurrence, "make_model"
    ].unique()

    output_df = []

    for make_model in matched_make_models:
        # Find the corresponding thefts value from top10theft
        top10_row = top10theft[
            top10theft["Model"].str.lower().str.startswith(make_model[:3])
        ]
        if not top10_row.empty:
            thefts_value = top10_row.iloc[0]["Thefts"]
            output_df.append(
                {
                    "Theft_Occurrence": theft_occurrence,
                    "Make_Model": make_model,
                    "Thefts": thefts_value,
                },
            )
    output_csv_filename = f"theft_occurrences_{theft_occurrence}.csv"
    output_df.to_csv(output_csv_filename, index=False)
    print(
        f"Results for theft occurrence {theft_occurrence} have been saved to {output_csv_filename}"
    )

# Step 4: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5: Impute missing values in y_train and y_test
imputer = SimpleImputer(strategy="mean")
y_train_imputed = imputer.fit_transform(y_train.values.reshape(-1, 1)).ravel()
y_test_imputed = imputer.transform(y_test.values.reshape(-1, 1)).ravel()

# Step 6: Train the machine learning model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train_imputed)

# Step 7: Make predictions
y_pred = model.predict(X_test)

# Step 8: Evaluate the model
mse = mean_squared_error(y_test_imputed, y_pred)
output_df = pd.DataFrame(columns=["Mean Squared Error"], data=[mse])
output_csv_filename = "mse_evaluation.csv"
output_df.to_csv(output_csv_filename, index=False)
print(f"Mean Squared Error has been saved to {output_csv_filename}")

# Example of predicting theft rate for new data
# Assuming 'new_data_features' contains features of new vehicles
new_data_features = X_test.head(9)  # Use the first row of the test set as an example
new_data_theft_rate = model.predict(new_data_features)
print("Predicted theft rate for new data:", new_data_theft_rate)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train the Gradient Boosting Regressor model
model = GradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
output_df = pd.DataFrame(columns=["Mean Squared Error"], data=[mse])
output_csv_filename = "gradient_boosting_mse_evaluation.csv"
output_df.to_csv(output_csv_filename, index=False)
print(
    f"Mean Squared Error for Gradient Boosting Regressor has been saved to {output_csv_filename}"
)

# Visualize the feature importances
feature_importances = model.feature_importances_
sorted_indices = np.argsort(feature_importances)[::-1]
sorted_features = X.columns[sorted_indices]
sorted_importances = feature_importances[sorted_indices]

output_df = pd.DataFrame(
    {"Feature": sorted_features, "Feature Importance": sorted_importances}
)
output_csv_filename = "feature_importance_visualization.csv"
output_df.to_csv(output_csv_filename, index=False)
print(f"Feature importances visualization has been saved to {output_csv_filename}")
