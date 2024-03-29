import pandas as pd
from ..utilities import logger

# Initialize logger
logger = logger.SmareLogger()

def m4_riskscores(car_listings):
    try:
        if not isinstance(car_listings, list):
            car_listings = [car_listings] 
            logger.warning("Model 4: Input is not a list. Converting to a list.")
        
        if len(car_listings) == 0:
            logger.error("Model 4: Input list is empty.")
            return []

        all_models = [data.get('model') for data in car_listings]
        models_df = pd.DataFrame(all_models, columns=['model'])
        model_frequency = models_df['model'].value_counts()
        max_frequency = model_frequency.max()
        risk_scores = []
        processed_listings = 0  

        for model, frequency in model_frequency.items():
            try:
                logger.debug(f"Model 4: Processing listing {processed_listings + 1}/{len(car_listings)}")
                processed_listings += frequency
                risk_score = frequency / max_frequency
                risk_score = max(0, min(1, risk_score))
                risk_scores.extend([risk_score] * frequency)
            except Exception as e:
                logger.error(f"Model 4: Error processing listing: {e}")

        if len(car_listings) != processed_listings:
            logger.error("Model 4: Input and output array sizes do not match.")
            return [-1] * len(car_listings)  
        return risk_scores
            
    except Exception as e:
        logger.error(f"Model 4: Error in M4 model: {e}")
        return [-1] * len(car_listings)  
