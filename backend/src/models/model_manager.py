from .m6_anomaly import m6_labels, preprocess_listing
import joblib

from ..utilities import logger
from ..utilities.database import (find_pending_risk_update,
                                  find_unanalyzed_cars, update_db_risk_scores,
                                  update_listing_scores)
# form m1_sentiment import m1_riskscores
from .m2_gptvision import m2_riskscores
from .m3_kbbprice import m3_riskscores
from .m4_carfreq import m4_riskscores
from .m5_theftlikelihood import m5_riskscores

MODEL_VERSIONS = [
    1, # Model 1: Sentiment Analysis Model
    1, # Model 2: GPT Vision Model
    1, # Model 3: KBB Price Model
    1, # Model 4: Car Frequency Model
    1, # Model 5: Theft Likelihood Model
    1, # Model 6: Luxury Model
    1, # Model 7: Anomaly Model
]

MODEL_WEIGHTS = [
    0,  # Model 1: Sentiment Analysis Model
    60, # Model 2: GPT Vision Model
    40, # Model 3: KBB Price Model
    10, # Model 4: Car Frequency Model
    20, # Model 5: Theft Likelihood Model
    10, # Model 6: Luxury Model
]

logger = logger.SmareLogger()


def filter_on_model(all_cars, model_num):
    try:
        return [car for car in all_cars if car["model_scores"][f"model_{model_num}"] == -1 or (f"model_{model_num}" in car["model_versions"] and car["model_versions"][f"model_{model_num}"] != MODEL_VERSIONS[model_num - 1])]
    except Exception as e:
        logger.critical(f"Model Manager: Could not filter cars for model_{model_num}. Error: {e}")
        return None


def update_risk_scores():
    try:
        listings_to_update = find_pending_risk_update()

        for i, car in enumerate(listings_to_update):
            new_score = -1

            for i, score in enumerate(car["model_scores"].values()):
                if score < 0:
                    continue

                if new_score < 0:
                    new_score = 0

                new_score += score * MODEL_WEIGHTS[i]

            listings_to_update[i]["risk_score"] = max(new_score, 100)
            listings_to_update[i]["pending_risk_update"] = False

        return update_db_risk_scores(listings_to_update)
    except Exception as e:
        logger.critical(f"Failed to update risk scores. Error: {e}")
        return None


# todo: calculate post-weight-product scores here, and not in each individual function.
# todo: check the time stamp periodically and stop execution after reaching the time stamp
def run(termination_timestamp):
    logger.info("Starting Model Manager...")

    # Importing data from MongoDB
    logger.info("Model Manager: Importing data from MongoDB...")
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
            model_2_cars = filter_on_model(all_cars, 2)
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
    try:
        success=1
        try:
            model_3_cars = filter_on_model(all_cars, 3)
            if not model_3_cars:
                logger.error("Model Manager: No cars to process for Model 3.")
                success= 0
        except Exception as e:
            logger.error(
                f"Model Manager: Model 3 failed to filter listings. Error: {e}"
            )
            return
        if(success):
            input_size = len(model_3_cars)
            logger.info(f"Model Manager: Model 3 started processing {input_size} listings")
            update_listing_scores(model_3_cars, m3_riskscores(model_3_cars), 3, MODEL_VERSIONS[2])
            logger.success("Model Manager: Model 3 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 3 failed to process listings. Error: {e}")


    # Model 4: Car Frequency Model
    try:
        success=1
        try:
            model_4_cars = filter_on_model(all_cars, 4)
            if not model_4_cars:
                logger.error("Model Manager: No cars to process for Model 4.")
                success= 0
        except Exception as e:
            logger.error(
                f"Model Manager: Model 4 failed to filter listings. Error: {e}"
            )
            return
        if(success):
            input_size = len(model_4_cars)
            logger.info(f"Model Manager: Model 4 started processing {input_size} listings")
            update_listing_scores(model_4_cars, m4_riskscores(model_4_cars), 4, MODEL_VERSIONS[3])
            logger.success("Model Manager: Model 4 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 4 failed to process listings. Error: {e}")


    # Model 5: Theft Likelihood Model
    try:
        success= 1
        try:
            model_5_cars = filter_on_model(all_cars, 5)  # Filter cars for model 5
            if not model_5_cars:
                logger.error("Model Manager: No cars to process for Model 5.")
                success= 0
        except Exception as e:
            logger.error(f"Model Manager: Model 5 failed to filter listings. Error: {e}")
            return
        if(success):
            input_size = len(model_5_cars)
            logger.info(f"Model Manager: Model 5 started processing {input_size} listings")
            theft_likelihoods = m5_riskscores(model_5_cars)
            update_listing_scores(model_5_cars, theft_likelihoods, 5, MODEL_VERSIONS[4])
            logger.success("Model Manager: Model 5 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 5 failed to process listings. Error: {e}")

    #Model 6: Anomaly/Luxury Model
    try:
        # Assuming the filter_on_model function is already defined
        model_6_cars = filter_on_model(all_cars, 6)
        if not model_6_cars:
            logger.error("Model Manager: No cars to process for Model 6.")
            return

        input_size = len(model_6_cars)
        logger.info(f"Model Manager: Model 6 started processing {input_size} listings.")

        # Load the model and preprocessor for Model 6
        try:
            model_6 = joblib.load('./src/models/isolation_forest_model.pkl')
            preprocessor_6 = joblib.load('./src/models/preprocessor.pkl')
        except Exception as e:
            logger.error(f"Model Manager: Failed to load Model 6 components. Error: {e}")
            return

        # Process listings with Model 6
        model_6_predictions = []
        for listing in model_6_cars:
            try:
                preprocessed_listing = preprocess_listing(listing)
                features_preprocessed = preprocessor_6.transform(preprocessed_listing)
                score = model_6.decision_function(features_preprocessed)
                prediction = 1 if score <= 0.05 else 0
                model_6_predictions.append(prediction)
            except Exception as e:
                logger.warning(f"Error processing listing for Model 6: {e}")
                model_6_predictions.append(-1)

        # Update scores in database
        update_listing_scores(model_6_cars, m6_labels(model_6_cars), 6, MODEL_VERSIONS[5])
        logger.success("Model Manager: Model 6 successfully processed listings.")
    except Exception as e:
        logger.error(f"Model Manager: Model 6 failed. Error: {e}")

    logger.success("Model Manager: All models successfully processed listings")

    try:
        update_count = update_risk_scores()

        logger.success(f"Updated {update_count} risk scores")
    except Exception as e:
        logger.error(f"Failed updating risk scores. Error: {e}")
