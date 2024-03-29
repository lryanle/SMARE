# Importing the M3_riskscores and M4_riskscores functions from their respective modules
# form m1_sentiment import m1_riskscores
from .m2_gptvision import m2_riskscores

# from m3_kbbprice import m3_riskscores
# from m4_carfreq import m4_riskscores

# from .m6_anomaly import m6_labels, preprocess_listing
import joblib

from ..utilities import logger
from ..utilities.database import find_unanalyzed_cars, update_listing_scores

MODEL_VERSIONS = [
    1, # Model 1: Sentiment Analysis Model
    1, # Model 2: GPT Vision Model
    1, # Model 3: KBB Price Model
    1, # Model 4: Car Frequency Model
    1, # Model 5: Theft Likelihood Model
    1, # Model 6: Luxury Model
    1, # Model 7: Anomaly Model
]

logger = logger.SmareLogger()


def filter_on_model(all_cars, model):
    try:
        return [car for car in all_cars if car["model_scores"][model] == -1]
    except Exception as e:
        logger.critical(f"Model Manager: Could not filter cars for {model}")
        return None

# todo: calculate post-weight-product scores here, and not in each individual function.
# todo: check the time stamp periodically and stop execution after reaching the time stamp
def run(termination_timestamp):
    logger.info("Starting Model Manager...")

    # Importing data from MongoDB
    logger.info("Moddel Manager: Importing data from MongoDB...")
    try:
        all_cars = find_unanalyzed_cars(MODEL_VERSIONS)
    except Exception as e:
        logger.critical(
            f"Model Manager: Failed to import data from MongoDB. Error: {e}"
        )
        return
    logger.success("Model Manager: Data successfully imported from MongoDB")

    # Model 1: Sentiment Analysis Model
    # here...

    # Model 2: GPT Vision Model
    try:
        try:
            model_2_cars = filter_on_model(all_cars, "model_2")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 2 failed to filter listings. Error: {e}"
            )
            return
        input_size = len(model_2_cars)

        logger.info(f"Model Manager: Model 2 started processing {input_size} listings")

        update_listing_scores(model_2_cars, m2_riskscores(model_2_cars), 2, MODEL_VERSIONS[1])

        logger.success("Model Manager: Model 2 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 2 failed to process listings. Error: {e}")

    # Model 3: KBB Price Model
    # here...

    # Model 4: Car Frequency Model
    # here...

    # Model 5: Theft Likelihood Model
    # here...

    # Model 6: Anomaly/Luxury Model
    # try:
    #     # Assuming the filter_on_model function is already defined
    #     model_6_cars = filter_on_model(all_cars, "model_6")
    #     if not model_6_cars:
    #         logger.error("Model Manager: No cars to process for Model 6.")
    #         return

    #     input_size = len(model_6_cars)
    #     logger.info(f"Model Manager: Model 6 started processing {input_size} listings.")

    #     # Load the model and preprocessor for Model 6
    #     try:
    #         model_6 = joblib.load('isolation_forest_model.pkl')
    #         preprocessor_6 = joblib.load('preprocessor.pkl')
    #     except Exception as e:
    #         logger.error(f"Model Manager: Failed to load Model 6 components. Error: {e}")
    #         return

    #     # Process listings with Model 6
    #     model_6_predictions = []
    #     for listing in model_6_cars:
    #         try:
    #             preprocessed_listing = preprocess_listing(listing)
    #             features_preprocessed = preprocessor_6.transform(preprocessed_listing)
    #             score = model_6.decision_function(features_preprocessed)
    #             prediction = 1 if score <= 0.05 else 0
    #             model_6_predictions.append(prediction)
    #         except Exception as e:
    #             logger.warning(f"Error processing listing for Model 6: {e}")
    #             model_6_predictions.append(-1)

    #     # Update scores in database
    #     update_listing_scores(model_6_cars, m6_labels(model_6_cars), 6, MODEL_VERSIONS[5])
    #     logger.success("Model Manager: Model 6 successfully processed listings.")
    # except Exception as e:
    #     logger.error(f"Model Manager: Model 6 failed. Error: {e}")

    logger.success("Model Manager: All models successfully processed listings")

run(0)