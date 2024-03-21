# Importing the M3_riskscores and M4_riskscores functions from their respective modules
# form m1_sentiment import m1_riskscores
from m2_gptvision import m2_riskscores
from m3_kbbprice import m3_riskscores
from m4_carfreq import m4_riskscores

from ..utilities import logger
from ..utilities.database import find_unanalyzed_cars

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
        return [car for car in all_cars if car[model] == -1]
    except Exception as e:
        logger.critical(f"Model Manager: Could not filter cars for {model}")
        return None


def append_to_cars(model_num, model_cars, scores):
    try:
        scored_model_cars = model_cars
        for car, score in zip(model_cars, scores):
            car.update({f"model_{model_num}": score, "model_versions": {f"model_{model_num}": MODEL_VERSIONS[model_num - 1]}})

        return scored_model_cars
    except Exception as e:
        logger.critical(f"Model Manager: Could append scores to model {model_num}")
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
    try:
        try:
            model_1_cars = filter_on_model(all_cars, "model_1")

        except Exception as e:
            logger.error(
                f"Model Manager: Model 1 failed to filter listings. Error: {e}"
            )
            return
        input_size = len(model_1_cars)

        logger.info(f"Model Manager: Model 1 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m1_results = m1_riskscores()
        # model_1_cars = append_to_cars(1, model_1_cars, m1_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 1 processing not implemented yet")
        logger.warning("Modem Manager: Model 1 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 1 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 1 failed to process listings. Error: {e}")

    # Model 2: GPT Vision Model
    try:
        try:
            model_2_cars = filter_on_model(all_cars, "model_2")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 2 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 2 started processing {input_size} listings")

        m2_results = m2_riskscores()
        model_2_cars = append_to_cars(1, model_2_cars, m2_results)

        logger.success("Model Manager: Model 2 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 2 failed to process listings. Error: {e}")

    # Model 3: KBB Price Model
    try:
        try:
            model_3_cars = filter_on_model(all_cars, "model_3")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 3 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 3 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m3_results = m3_riskscores()
        # model_3_cars = append_to_cars(1, model_3_cars, m3_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 3 processing not implemented yet")
        logger.warning("Modem Manager: Model 3 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 3 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 3 failed to process listings. Error: {e}")

    # Model 4: Car Frequency Model
    try:
        try:
            model_4_cars = filter_on_model(all_cars, "model_4")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 4 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 4 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m4_results = m4_riskscores()
        # model_4_cars = append_to_cars(1, model_4_cars, m4_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 4 processing not implemented yet")
        logger.warning("Modem Manager: Model 4 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 4 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 4 failed to process listings. Error: {e}")

    # Model 5: Theft Likelihood Model
    try:
        try:
            model_5_cars = filter_on_model(all_cars, "model_5")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 5 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 5 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m4_results = m4_riskscores()
        # model_5_cars = append_to_cars(1, model_5_cars, m5_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 5 processing not implemented yet")
        logger.warning("Modem Manager: Model 5 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 5 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 5 failed to process listings. Error: {e}")

    # Model 6: Luxury Model
    try:
        try:
            model_6_cars = filter_on_model(all_cars, "model_6")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 6 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 6 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m4_results = m4_riskscores()
        # model_6_cars = append_to_cars(1, model_6_cars, m6_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 6 processing not implemented yet")
        logger.warning("Modem Manager: Model 6 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 6 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 6 failed to process listings. Error: {e}")

    # Model 7: Anomaly Model
    try:
        try:
            model_7_cars = filter_on_model(all_cars, "model_7")
        except Exception as e:
            logger.error(
                f"Model Manager: Model 7 failed to filter listings. Error: {e}"
            )
            return
        input_size = 0

        logger.info(f"Model Manager: Model 7 started processing {input_size} listings")

        # todo: upload updated results back to mongodb
        # m4_results = m4_riskscores()
        # model_1_cars = append_to_cars(1, model_1_cars, m1_results) # appends scores to the filtered cars list of this model

        # REMOVE ME
        logger.warning("Model Manager: Model 7 processing not implemented yet")
        logger.warning("Modem Manager: Model 7 isn't yet tagging results with its version")

        logger.success("Model Manager: Model 7 successfully processed listings")
    except Exception as e:
        logger.error(f"Model Manager: Model 7 failed to process listings. Error: {e}")

    logger.success("Model Manager: All models successfully processed listings")
