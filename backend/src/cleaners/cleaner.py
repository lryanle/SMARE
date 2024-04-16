import os
from datetime import datetime

from ..utilities import database as db
from ..utilities import logger
from . import craigslist as cl
from . import facebook as fb
from . import utils

logger = logger.SmareLogger()

CONSECUTIVE_ERROR_LIMIT = int(os.environ.get("CLEAN_CONS_ERR_LIMIT", 20))


class MakeModelException(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)


def clean(car):
    try:
        clean_car = {}

        if car["source"] == "facebook":
            if "attributes" in car:
                clean_car["attributes"] = fb.extract_attributes(car["attributes"])
            clean_car["year"] = utils.extract_year(car["title"])
            clean_car["make"] = utils.extract_make(car["title"])
            clean_car["model"] = fb.extract_model(car["title"], clean_car["make"])
        elif car["source"] == "craigslist":
            if "attributes" in car:
                clean_car["attributes"] = cl.extract_attributes(car["attributes"])

            if "makemodel" in car:
                clean_car["make"] = utils.extract_make(car["makemodel"])
                clean_car["model"] = cl.extract_model(car["makemodel"], clean_car["make"])
            else:
                clean_car["make"] = utils.extract_make(car["title"])
                clean_car["model"] = cl.extract_model(car["title"], clean_car["make"])

            clean_car.update(cl.str_to_num(car))

        if "attributes" not in clean_car and "attributes" not in car:
            logger.warning(f"Attributes not found in car {car['_id']}")

        if not clean_car["make"]:
            logger.debug(f"car: {car['makemodel']}")
            raise MakeModelException("Failed cleaning make")

        if not clean_car["model"]:
            logger.debug(f"car {clean_car['make']}: {car['makemodel']}")
            raise MakeModelException("Failed cleaning model")

        clean_car["price"] = utils.clean_currency(car["price"])

        if "attributes" in clean_car and "odometer" in clean_car["attributes"] and isinstance(clean_car["attributes"]["odometer"], int):
            clean_car["odometer"] = clean_car["attributes"]["odometer"]
        else:
            clean_car["odometer"] = utils.clean_odometer(car["odometer"])

        return clean_car
    except MakeModelException as error:
        logger.warning(f"Error extracting make and mode: {error}")
        return None
    except Exception as error:
        logger.error(f"Error cleaning car data: {error}")
        return None


def check(car):
    required_checks = [
        "price" in car and car["price"] > 0,
        "odometer" in car and car["odometer"] > 0,
        "year" in car and car["year"] >= 2000,
        "make" in car,
        "model" in car,
    ]

    logger.debug(f"Checks: {required_checks}")

    return False not in required_checks


def run(termination_timestamp, version):
    cars = db.find_cars_in_stage("scrape")

    logger.info("Began cleaners")
    logger.info(f"Found {len(cars)} unclean cars")

    total_cleaned = 0
    total_errs = 0
    consecutive_errs = 0

    for car in cars:
        try:
            clean_fields = clean(db.decode(car))
            if clean_fields and check(clean_fields):
                clean_fields["stage"] = "clean"
                clean_fields["cleaner_version"] = version

                clean_fields["model_scores"] = {}
                clean_fields["model_versions"] = {}
                for i in range(1, 8):
                    clean_fields["model_scores"][f"model_{i}"] = -1
                    clean_fields["model_versions"][f"model_{i}"] = -1
                clean_fields["risk_score"] = -1

                is_update_sucess = db.update(car["link"], clean_fields)

                if not is_update_sucess:
                    raise ValueError("Failed updating the database.")

                logger.info(f"Cleaned _id: {car['_id']}")
                total_cleaned += 1
                consecutive_errs = 0
            else:
                raise ValueError("Cleaned fields were not generated due to an error.")
        except Exception as error:
            total_errs += 1
            consecutive_errs += 1
            logger.error(f"Failed cleaning _id: {car['_id']} | Error: {error}")

            if consecutive_errs >= CONSECUTIVE_ERROR_LIMIT:
                logger.critical(
                    f"Cleaner failed {consecutive_errs} times in a row. Stopping cleaner early."
                )
                break

        if datetime.now() >= termination_timestamp:
            logger.info("Cleaning process is done.")
            break

    logger.info(
        f"Cleaning summary: {total_errs} errors, {total_cleaned} cleaned"
        f"{len(cars) - total_cleaned} unreached (due to errors or incomplete processing)."
    )


def __init__():
    logger.info("Cleaner initialized")
