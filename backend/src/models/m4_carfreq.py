import pandas as pd
from ..utilities import logger

# Initialize logger
logger = logger.SmareLogger()

def m4_riskscores(listings):
    logger.info("Starting M4 model for calculating risk scores...")
    output = []

    for k, listing in enumerate(listings):
        try:
            logger.debug(f"Model 4: Processing listing {k + 1}/{len(listings)}")
            model = listing.get('model')

            if model is not None:
                all_models = [listing['model'] for listing in listings]
                models_df = pd.DataFrame(all_models, columns=['model'])
                model_frequency = models_df['model'].value_counts()
                max_frequency = model_frequency.max()

                risk_scores = []
                for model, frequency in model_frequency.items():
                    risk_score = frequency / max_frequency            
                    risk_score = max(0, min(1, risk_score))
                    risk_scores.append(risk_score)
                output.append(risk_scores)
            else:
                logger.warning("Model information not found in the listing.")
                output.append([])
        except Exception as e:
            logger.warning(f"Error with model 4: {e}")
            output.append(-1)
            continue

    logger.info("M4 model execution completed successfully.")
    return output
