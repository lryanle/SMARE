import json
from difflib import SequenceMatcher
from ..utilities.logger import SmareLogger

# Initialize logger
logger = SmareLogger()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_theft(make, model, year, data):
    theft_rate = 0
    max_similarity = 0
    input_string = f"{year} {make} {model}"
    for entry in data:
        entry_string = f"{entry['year']} {entry['manufacturer']} {entry['make']} {entry['make_model']}"
        similarity_score = similar(input_string.lower(), entry_string.lower())
        entry_year = int(entry['year'])
        if abs(entry_year - year) <= 5:
            if similarity_score > max_similarity:
                max_similarity = similarity_score
                theft_rate = float(entry["rate"])
    return theft_rate

def get_theft_rates(cars_listings, theft_data_file):
    with open(theft_data_file, "r") as file:
        theft_data = json.load(file)
    theft_rates = []
    for k, car in enumerate(cars_listings):
        try:
            logger.debug(f"Model 5: Processing listing {k + 1}/{len(cars_listings)}")
            make = car["make"]
            model = car["model"]
            year = car["year"]
            theft_rate = get_theft(make, model, year, theft_data)
            theft_rates.append(theft_rate)  
        except Exception as e:
            logger.warning(f"Error occurred with Model 5: {str(e)}")
            theft_rates.append(-1)  
    logger.debug("Successfully calculated theft rates.")
    return theft_rates
    

def calculate_likelihoods(theft_rates):
    theft_likelihoods = []
    for theft_rate in theft_rates:
        try:
            risk_score = theft_rate / 100 if theft_rate is not None else 0
            theft_likelihoods.append(risk_score)  
        except Exception as e:
            logger.error(f"Model 5: Failed to calculate risk score: {e}")
            theft_likelihoods.append(-1)  
    return theft_likelihoods

def m5_riskscores(cars_listings):
    try:
        theft_rates = get_theft_rates(cars_listings, "/var/task/src/models/nhtsa_theft_data.json")
        theft_likelihoods = calculate_likelihoods(theft_rates)
        logger.info("Model 5: M5 model execution completed successfully.")
        return theft_likelihoods
    except Exception as e:
        logger.error(f"Model 5: An error occurred: {e}")
        return [-1] * len(cars_listings)  
    
