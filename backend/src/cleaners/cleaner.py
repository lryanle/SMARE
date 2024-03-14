from .. import database as db
from . import facebook as fb
from . import utils

CONSECUTIVE_ERROR_LIMIT = 3


def clean(car):
    clean_car = {}

    if car["source"] == "facebook":
        clean_car["attributes"] = fb.extract_attributes(car["attributes"])
    elif car["source"] == "craigslist":
        # TODO: Modularize craigslist cleaner
        print("Craigslist car")

    clean_car["price"] = utils.clean_currency(car["price"])

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
            clean_fields["cleaner-version"] = version

            db.update(car["link"], clean_fields)
            logger(f"cleaned _id: {car['_id']}")

            total_cleaned += 1
            consecutive_errs = 0
        except Exception as error:
            total_errs += 1
            consecutive_errs += 1

            logger(f"failed cleaning _id: {car['_id']}\n{error}")

            if consecutive_errs >= CONSECUTIVE_ERROR_LIMIT:
                logger(f"cleaner failed {consecutive_errs} in a row. Stopping cleaner early.")
                break

        if is_done:
            break

    logger(f"cleaning summary: {total_errs} errors, {total_cleaned} cleaned,"
           f" {len(cars) - total_errs - total_cleaned} unreached")

def __init__():
    print("cleaner initialized")