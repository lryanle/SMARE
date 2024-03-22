# Importing the M3_riskscores and M4_riskscores functions from their respective modules
# form m1_sentiment import m1_riskscores
from .m2_gptvision import m2_riskscores

# from m3_kbbprice import m3_riskscores
# from m4_carfreq import m4_riskscores

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
def run(timestamp):
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
    # here...

    logger.success("Model Manager: All models successfully processed listings")

run(0)
