from ..utilities import logger
from .utils import clean_odometer, extract_year
from .utils import extract_model as model_parser

logger = logger.SmareLogger()


def extract_attributes(attributes):
    output = {}

    try:
        # Extract attributes using regular expressions
        for attr_obj in attributes:
            if attr_obj["label"] == "odometer":
                output["odometer"] = clean_odometer(attr_obj["value"])
            else:
                output[attr_obj["label"]] = attr_obj["value"]
    except Exception as e:
        logger.error(f"Error extracting attributes: {e}")

    return output


def str_to_num(car):
    clean_car = {}

    try:
        if "year" in car:
            clean_car["year"] = int(car["year"])
        else:
            clean_car["year"] = extract_year(car["title"])

        if "latitude" in car and "longitude" in car:
            clean_car["latitude"] = float(car["latitude"])
            clean_car["longitude"] = float(car["longitude"])
    except ValueError as e:
        logger.error(f"Error converting string to number for car: {car['_id']} | Error: {e}")
    except KeyError as e:
        logger.error(
            f"Key missing when converting string to number for car: {car['_id']} | Error: {e}"
        )

    return clean_car


def extract_model(title, make):
    try:
        return model_parser(title, make, r"\w+\s+(.*)")
    except Exception as e:
        logger.error(f"Error extracting model from title {title}: {e}")
        return None
