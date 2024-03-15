from ..utils import database as db
from . import facebook as fb
from . import craigslist as cl
from . import utils

CONSECUTIVE_ERROR_LIMIT = 3


def clean(car):
    clean_car = {}

    if car["source"] == "facebook":
        clean_car["attributes"] = fb.extract_attributes(car["attributes"])
    elif car["source"] == "craigslist":
        clean_car["attributes"] = cl.extract_attributes(car["attributes"])
        clean_car.update(cl.str_to_num(car))

    clean_car["price"] = utils.clean_currency(car["price"])
    clean_car["odometer"] = clean_car["attributes"]["odometer"]

    return clean_car


def run(logger, is_done, version):
    cars = db.find_cars_in_stage("scrape")

    logger("began cleaners")
    logger(f"found {len(cars)} unclean cars")

    total_cleaned = 0
    total_errs = 0
    consecutive_errs = 0

    for car in cars:
        try:
            clean_fields = clean(db.decode(car))
            clean_fields["stage"] = "clean"
            clean_fields["cleaner_version"] = version

            clean_fields["model_1"] = -1
            clean_fields["model_2"] = -1
            clean_fields["model_3"] = -1
            clean_fields["model_4"] = -1
            clean_fields["model_5"] = -1
            clean_fields["model_6"] = -1
            clean_fields["model_7"] = -1

            db.update(car["link"], clean_fields)
            logger(f"cleaned _id: {car['_id']}")

            total_cleaned += 1
            consecutive_errs = 0
        except Exception as error:
            total_errs += 1
            consecutive_errs += 1

            logger(f"failed cleaning _id: {car['_id']}\n{error}")

            if consecutive_errs >= CONSECUTIVE_ERROR_LIMIT:
                logger(
                    f"cleaner failed {consecutive_errs} in a row. Stopping cleaner early."
                )
                break

        if is_done:
            break

    logger(
        f"cleaning summary: {total_errs} errors, {total_cleaned} cleaned,"
        f" {len(cars) - total_errs - total_cleaned} unreached"
    )


def __init__():
    print("cleaner initialized")
