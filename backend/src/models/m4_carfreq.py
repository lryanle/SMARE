import json
import pandas as pd
from ..utilities import logger

# Initialize logger
logger = logger.SmareLogger()

def m4_riskscores(car_listings):
    # VEHICLE FREQUENCY MODEL
    try:
        logger.info("Starting M4 model for calculating risk scores...")
        # Ensure the input is a list even if it's a single object
        if not isinstance(car_listings, list):
            car_listings = [car_listings]  # Convert single object input to list
            logger.warning("Input is not a list. Converting to a list.")  
        if len(car_listings) == 0:
            logger.error("Input list is empty.")
            return []
        
        # Accumulate all the models into a list
        all_models = []
        for data in car_listings:
            # Extract relevant data
            model = data.get('model')
            all_models.append(model)

        # Create a DataFrame from the list of models
        models_df = pd.DataFrame(all_models, columns=['model'])

        # Analyze frequency of vehicle models
        model_frequency = models_df['model'].value_counts()
        max_frequency = model_frequency.max()
        
        # Calculate risk score for each model and append to the list
        risk_scores = []
        for model, frequency in model_frequency.items():
            risk_score = frequency / max_frequency            
            # Ensure risk score is between 0 and 1
            risk_score = max(0, min(1, risk_score))
            risk_scores.append(risk_score)
            logger.info(f"Risk score calculated for model {model}: {risk_score}")

        return risk_scores
            
    except Exception as e:
        logger.error(f"Error in M3 model: {e}")
        return None
