import json
from difflib import SequenceMatcher
from ..utilities.logger import SmareLogger

# Initialize logger
logger = SmareLogger()
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_theft(make, model, year, data):
    theft_rate = None
    max_similarity = 0
    input_string = f"{year} {make} {model}"
    for entry in data:
        # Construct the string for the entry to be compared
        entry_string = f"{entry['year']} {entry['manufacturer']} {entry['make']} {entry['make_model']}"
        # Calculate similarity using the entire constructed strings
        similarity_score = similar(input_string.lower(), entry_string.lower())
        # Check if the year is within a 5-year range and the makes and models are similar
        entry_year = int(entry['year'])
        if abs(entry_year - year) <= 5:
            if similarity_score > max_similarity:
                max_similarity = similarity_score
                theft_rate = float(entry["rate"])
    return theft_rate

def get_theft_rates(cars_file, theft_data_file):
    try:
        with open(cars_file, "r") as file:
            cars_data = json.load(file)
        with open(theft_data_file, "r") as file:
            theft_data = json.load(file)
        theft_rates = []
        for car in cars_data:
            make = car["make"]
            model = car["model"]
            year = car["year"]
            theft_rate = get_theft(make, model, year, theft_data)
            theft_rates.append(theft_rate)  # Append theft rate to the list
        logger.info("Successfully calculated theft rates.")
        return theft_rates
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")


def calculate_likelihoods(theft_rates):
    theft_likelihoods = []
    for theft_rate in theft_rates:
        try:
            # Calculate risk score based on theft rate
            if theft_rate is not None:
                risk_score = theft_rate / 100  # Normalize theft rate to be between 0 and 1
                theft_likelihoods.append({"theft_rate": theft_rate, "risk_score": risk_score})
            else:
                theft_likelihoods.append({"theft_rate": None, "risk_score": -1})  # Append None if theft rate is not available for the listing
        except Exception as e:
            logger.error(f"Failed to calculate risk score: {e}")
            theft_likelihoods.append({"theft_rate": None, "risk_score": -1})  # Append -1 if calculation fails for the listing
    return theft_likelihoods

def m5_theftlikelihood(cars_file,theft_data_file = "nhtsa_theft_data.json"):
    try:
        logger.info("Starting M5 model for calculating theft likelihoods...")
      # Get theft rates
        theft_rates = get_theft_rates(cars_file, theft_data_file)
        # Calculate theft likelihoods
        theft_likelihoods = calculate_likelihoods(theft_rates)
        logger.info("M5 model execution completed successfully.")
        return theft_likelihoods
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []

#thefts_riskscore = m5_theftlikelihood("cars.json","nhtsa_theft_data.json")
