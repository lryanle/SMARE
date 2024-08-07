import os
from math import ceil

import joblib
from openai import RateLimitError

from ..sendGrid import notifs
from ..utilities import logger
from ..utilities.database import (find_pending_risk_update,
                                  find_unanalyzed_cars, update_db_risk_scores,
                                  update_listing_scores, connect)
from .m2_gptvision import m2_riskscores
from .m3_kbbprice import m3_riskscores
from .m4_carfreq import m4_riskscores
from .m5_theftlikelihood import m5_riskscores
from .m6_anomaly import m6_labels, preprocess_listing

MODEL_VERSIONS = [
    1, # Model 1: Sentiment Analysis Model
    2, # Model 2: GPT Vision Model
    1, # Model 3: KBB Price Model
    1, # Model 4: Car Frequency Model
    1, # Model 5: Theft Likelihood Model
    1, # Model 6: Luxury Model
    1, # Model 7: Anomaly Model
]

MODEL_WEIGHTS = [int(w) for w in os.environ.get("MODEL_WEIGHTS", "0,60,40,10,20,10,0").split(",")]
BATCH_SIZE = int(os.environ.get("MODEL_BATCH_SIZE", 15))

logger = logger.SmareLogger()

flagged_listings = []

def filter_on_model(all_cars, model_num):
    try:
        return [car for car in all_cars if car["model_scores"][f"model_{model_num}"] == -1 or (f"model_{model_num}" in car["model_versions"] and car["model_versions"][f"model_{model_num}"] != MODEL_VERSIONS[model_num - 1])]
    except Exception as e:
        logger.critical(f"Model Manager: Could not filter cars for model_{model_num}. Error: {e}")
        return None


def update_risk_scores(conn):
    try:
        listings_to_update = find_pending_risk_update(conn)
        logger.info(f"Found {len(listings_to_update)} that can be re-evaluated")

        for car in listings_to_update:
            if "model_scores" not in car:
                logger.error(f"Listing with id: {car['_id']} (stage: '{car['stage']}') does not have 'model_scores' property")
                car["risk_score"] = -1
                continue

            new_risk_score = car["risk_score"]

            for i, model_score in enumerate(car["model_scores"].values()):
                if model_score < 0:
                    continue

                new_risk_score = max(new_risk_score, 0)
                new_risk_score += model_score * MODEL_WEIGHTS[i]

            if new_risk_score >= 0:
                car["risk_score"] = min(new_risk_score, 100)
                car["pending_risk_update"] = False
            if new_risk_score > 50:
                flagged_listings.append(car)
        return update_db_risk_scores(conn, listings_to_update), listings_to_update
    except Exception as e:
        logger.critical(f"Failed to update risk scores. Error: {e}")
        return None


def batch_process(conn, model_cars, model_fn, model_num):
    num_of_cars = len(model_cars)

    for i in range(0, num_of_cars, BATCH_SIZE):
        batch = model_cars[i:i + BATCH_SIZE]

        logger.info(f"Model {model_num} processing batch {int(i/BATCH_SIZE) + 1}/{ceil(num_of_cars/BATCH_SIZE)}")
        update_listing_scores(conn, batch, model_fn(batch), model_num, MODEL_VERSIONS[model_num - 1])


# todo: calculate post-weight-product scores here, and not in each individual function.
# todo: check the time stamp periodically and stop execution after reaching the time stamp
def run(termination_timestamp):
    logger.info("Starting Model Manager...")

    # Importing data from MongoDB
    logger.info("Model Manager: Importing data from MongoDB...")
    try:
        conn = connect()

        if not conn:
             raise Exception("Failed connecting to DB for model manager")

        all_cars = find_unanalyzed_cars(conn, MODEL_VERSIONS)
    except Exception as e:
        logger.critical(
            f"Model Manager: Failed to import data from MongoDB. Error: {e}"
        )
        return
    logger.success("Model Manager: Data successfully imported from MongoDB")


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
            batch_process(model_4_cars, m4_riskscores, 4)
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
            batch_process(model_5_cars, m5_riskscores, 5)
            logger.success("Model Manager: Model 5 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 5 failed to process listings. Error: {e}")


    #Model 6: Anomaly/Luxury Model
    try:
        # Assuming the filter_on_model function is already defined
        model_6_cars = filter_on_model(all_cars, 6)
        if not model_6_cars:
            logger.error("Model Manager: No cars to process for Model 6.")

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
        update_listing_scores(conn, model_6_cars, m6_labels(model_6_cars), 6, MODEL_VERSIONS[5])
        logger.success("Model Manager: Model 6 successfully processed listings.")
    except Exception as e:
        logger.error(f"Model Manager: Model 6 failed. Error: {e}")

    logger.success("Model Manager: All models successfully processed listings")

    try:
        update_count, updated_listings = update_risk_scores(conn)

        logger.success(f"Updated {update_count} risk scores")
    except Exception as e:
        logger.error(f"Failed updating risk scores. Error: {e}")


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
            return None

        input_size = len(model_2_cars)

        logger.info(f"Model Manager: Model 2 started processing {input_size} listings")
        batch_process(model_2_cars, m2_riskscores, 2)

        logger.success("Model Manager: Model 2 successfully processed listings")
    except RateLimitError as e:
        logger.critical(f"Model Manager: Model 2 failed to process listings. Ran out of OpenAI credits {e}")
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
            batch_process(conn, model_3_cars, m3_riskscores, 3)

            logger.success("Model Manager: Model 3 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 3 failed to process listings. Error: {e}")


    try:
        update_count, new_updated_listings = update_risk_scores(conn)

        logger.success(f"Updated {update_count} risk scores")
    except Exception as e:
        logger.error(f"Failed updating risk scores. Error: {e}")


    updated_listings = updated_listings + new_updated_listings

    # Send daily email report
    #recipient_emails = ['dawsen_richins@yahoo.com','alsimone00@gmail.com','caitlynary@gmail.com', 'tadero230@gmail.com']
    recipient_emails = ['caitlynary@gmail.com', 'tadero230@gmail.com']
    notifs.send_daily_email_report(recipient_emails,updated_listings)
    logger.success("Model Manager: Successfully Emailed Recipent")

    # # Send flagged report notification for flagged listings
    # for flagged_listing in flagged_listings:
    #     notifs.send_flagged_report_notification(recipient_emails,flagged_listing)
    # logger.success("Model Manager Flagged: Successfully Emailed Recipent Flagged Report")
