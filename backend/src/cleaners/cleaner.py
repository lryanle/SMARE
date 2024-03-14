from .. import database as db
from . import facebook as fb
from . import utils


def clean(car):
    cleanCar = {}

    if car["source"] == "facebook":
        cleanCar["attributes"] = fb.extractAttributes(db.deencodeArr(car["attributes"]))
    elif car["source"] == "craigslist":
        # TODO: Modularize craigslist cleaner
        print("Craigslist car")

    cleanCar["price"] = utils.cleanCurrency(car["price"])

    return cleanCar


def run(logs, isDone):
    cars = db.findCarsInStage("scrape")

    for car in cars:
        cleanFields = clean(db.decode(car))
        cleanFields["stage"] = "clean"

        db.update(car["link"], cleanFields)

        logs["clean"]

        if isDone:
            break
    