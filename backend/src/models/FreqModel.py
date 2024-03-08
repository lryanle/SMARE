# import necessary libraries
import pandas as pd
import car_data

# VEHICLE FREQUENCY MODEL
cars_dff = car_data.cars


# Function to analyze frequency of vehicle models and calculate risk score
def calculate_risk_score(row, model_frequency, max_frequency, threshold=10):
    # Normalize model frequency
    risk_score = model_frequency[row["model"]] / max_frequency
    return round(risk_score, 4)  # Round up to 4 decimal places


# Analyze frequency of vehicle models
model_frequency = cars_dff["model"].value_counts()
max_frequency = model_frequency.max()

# Calculate risk score based on frequency for each row
cars_dff["risk_score"] = cars_dff.apply(
    lambda row: calculate_risk_score(row, model_frequency, max_frequency), axis=1
)

cars_dff = cars_dff.drop(columns=["source", "location", "title"])

# Save the results to a CSV file
output_csv_filename = "ModelFreq_results.csv"
cars_dff.to_csv(output_csv_filename, index=False)
print(f"Results have been saved to {output_csv_filename}")
