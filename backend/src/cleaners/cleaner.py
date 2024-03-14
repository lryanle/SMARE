from .. import database as db
from . import facebook as fb
from . import utils

CONSECUTIVE_ERROR_LIMIT = 3


def clean(car):
    cleanCar = {}

    if car["source"] == "facebook":
        cleanCar["attributes"] = fb.extractAttributes(car["attributes"])
    elif car["source"] == "craigslist":
        # TODO: Modularize craigslist cleaner
        print("Craigslist car")

    cleanCar["price"] = utils.cleanCurrency(car["price"])

    return cleanCar


def run(logger, isDone, version):
    cars = db.findCarsInStage("scrape")

    logger("began cleaners")
    logger(f"found {len(cars)} unclean cars")

    totalCleaned = 0
    totalErrs = 0
    consecutiveErrs = 0

    for car in cars:
        try:
            cleanFields = clean(db.decode(car))
            cleanFields["stage"] = "clean"
            cleanFields["cleaner-version"] = version

            db.update(car["link"], cleanFields)
            logger(f"cleaned _id: {car['_id']}")

            totalCleaned += 1
            consecutiveErrs = 0
        except Exception as error:
            totalErrs += 1
            consecutiveErrs += 1

            logger(f"failed cleaning _id: {car['_id']}\n{error}")

            if consecutiveErrs >= CONSECUTIVE_ERROR_LIMIT:
                logger(f"cleaner failed {consecutiveErrs} in a row. Stopping cleaner early.")
                break

        if isDone:
            break

    logger(f"cleaning summary: {totalErrs} errors, {totalCleaned} cleaned,"
           f" {len(cars) - totalErrs - totalCleaned} unreached")
