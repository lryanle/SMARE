import json
import re
from difflib import SequenceMatcher, get_close_matches

from ..utilities import logger

logger = logger.SmareLogger()


def clean_currency(price_str):
    try:
        clean_str = price_str.replace("$", "").replace(",", "")

        if clean_str.lower() == "free":
            clean_str = "0"

        return float(clean_str)
    except ValueError as e:
        logger.error(f"Error converting price to float: {price_str} | Error: {e}")
        return None


def clean_odometer(odometer_str):
    try:
        clean_str = odometer_str.replace("k", "000").replace(",", "").replace(" mi", "")
        return int(clean_str)
    except ValueError as e:
        logger.error(f"Error converting odometer to int: {odometer_str} | Error: {e}")
        return None


CAR_MAKES = [
    "acura",
    "alfa-romeo",
    "aston-martin",
    "audi",
    "bentley",
    "bmw",
    "buick",
    "cadillac",
    "chevrolet",
    "chrysler",
    "dodge",
    "ferrari",
    "fiat",
    "ford",
    "genesis",
    "gmc",
    "honda",
    "hyundai",
    "infiniti",
    "jaguar",
    "jeep",
    "kia",
    "lamborghini",
    "landrover",
    "lexus",
    "lincoln",
    "lucid",
    "maserati",
    "mazda",
    "mclaren",
    "mercedes-benz",
    "mini",
    "mitsubishi",
    "nissan",
    "polestar",
    "porsche",
    "ram",
    "rivian",
    "rolls-royce",
    "subaru",
    "tesla",
    "toyota",
    "volkswagen",
    "volvo",
]


def extract_make(title):
    try:
        for make in CAR_MAKES:
            if make.lower() in title.lower():
                return make.lower()

        return best_fitting_make(title)
    except Exception as e:
        logger.error(f"Error extracting make: {title} | Error: {e}")
        return None


def best_fitting_make(title):
    try:
        title_words = title.lower().split()
        max_similarity = 0
        best_match = None

        for make in CAR_MAKES:
            similarity = max(
                SequenceMatcher(None, make, word).ratio() for word in title_words
            )
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = make

        return best_match
    except Exception as e:
        logger.error(f"Error finding best fitting make: {title} | Error: {e}")
        return None


def extract_model(title, make, regex):
    try:
        with open("./src/utilities/car_models.json") as models_json:
            models = json.load(models_json)
            models = models[make.lower()]

        match = re.search(regex, title)

        if match:
            model_search_area = match.group(1)
            model_search_area = model_search_area.replace("-", "")

            close_match = get_close_matches(model_search_area, models, n=1, cutoff=0.4)
            if close_match:
                return close_match[0]

        return incremental_model_search(title, make, models)
    except json.JSONDecodeError as e:
        logger.error(f"Error reading car models JSON file: {e}")
        return None
    except Exception as e:
        logger.error(f"Error extracting model: {title}, {make} | Error: {e}")
        return None


def incremental_model_search(title, make, models):
    try:
        title_words = title.split(" ")
        search_substring = []

        for word in title_words:
            if word.lower() in make.lower():
                continue
            search_substring.append(word)

            close_match = get_close_matches(
                " ".join(search_substring), models, n=1, cutoff=0.1
            )

            if close_match:
                return close_match[0]

        return None
    except Exception as e:
        logger.error(f"Error in incremental model search: {title}, {make} | Error: {e}")
        return None
