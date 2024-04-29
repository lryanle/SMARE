import os
import re
from datetime import datetime
from urllib.parse import quote, unquote

from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient, UpdateOne
from pymongo.errors import ConfigurationError

from .logger import SmareLogger

DATABASE = "scrape"
SCRAPE_COLLECTION = "listings"
LOG_COLLECTION = "logs"

DONT_DECODE = ["link", "_id", "price", "odometer", "images"]

logger = SmareLogger()


def connect(db=DATABASE):
    try:
        load_dotenv()
    except Exception as e:
        logger.critical(f"Database: Failed to load .env file. Error: {e}")
        return {"success": False, "db": 0}

    try:
        db_uri = os.environ.get("DB_URI")
        client = MongoClient(db_uri)

    except ConfigurationError:
        logger.critical(
            "Database: "
            "An Invalid URI host error was received."
            " Is your Atlas host name correct in your connection string (found the .env)?"
        )
        return None

    return client

def get_conn(db=DATABASE):
    try:
        load_dotenv()
    except Exception as e:
        logger.critical(f"Database: Failed to load .env file. Error: {e}")
        return {"success": False, "db": 0}

    try:
        db_uri = os.environ.get("DB_URI")
        client = MongoClient(db_uri)

    except ConfigurationError:
        logger.critical(
            "Database: "
            "An Invalid URI host error was received."
            " Is your Atlas host name correct in your connection string (found the .env)?"
        )
        return {"success": False, "db": 0}

    return {"success": True, "db": client.get_database(db)}


def extract_id_from_link(link):
    try:
        id = re.search(r"^\d+$", link)
        facebook = re.search(r"facebook\.com/marketplace/item/(\d+)/", link)
        craigslist = re.search(r"/(\d+)\.html$", link)

        if id:
            return id

        if facebook:
            return facebook.group(1)

        if craigslist:
            return craigslist.group(1)
    except Exception as e:
        logger.error(f"Database: Failed to extract id from link. Error: {e}")
        return None


def find_cars_in_stage(client, stage):
    try:
        conn = client.get_database(DATABASE)

        return [
            decode(car) for car in conn[SCRAPE_COLLECTION].find({"stage": stage}).sort([("scrape_date", DESCENDING)])
        ]
    except Exception as e:
        logger.error(f"Database: Failed to find cars in stage. Error: {e}")
        return None


def find_unanalyzed_cars(client, current_versions):
    try:
        conn = client.get_database(DATABASE)

        query = {
            "stage": "clean",
            "$or": [
                {"$or": [
                    # {"model_scores.model_1": -1},
                    {"model_scores.model_2": -1},
                    {"model_scores.model_3": -1},
                    {"model_scores.model_4": -1},
                    {"model_scores.model_5": -1},
                    {"model_scores.model_6": -1},
                ]},
                {"$or": [
                    # {"model_versions.model_1": {"$not": {"$eq": current_versions[0]}}},
                    {"model_versions.model_2": {"$not": {"$eq": current_versions[1]}}},
                    {"model_versions.model_3": {"$not": {"$eq": current_versions[2]}}},
                    {"model_versions.model_4": {"$not": {"$eq": current_versions[3]}}},
                    {"model_versions.model_5": {"$not": {"$eq": current_versions[4]}}},
                    {"model_versions.model_6": {"$not": {"$eq": current_versions[5]}}},
                ]}
            ],
        }

        return [decode(car) for car in conn[SCRAPE_COLLECTION].find(query)]
    except Exception as e:
        logger.error(f"Database: Failed to find unanalyzed cars. Error: {e}")
        return None


def post_raw(client, scraper_version, source, car):
    logger.info("Database: Connecting to DB...")
    try:
        conn = client.get_database(DATABASE)

        if conn is not None:
            logger.error("Database (post_raw): Failed to connect to DB.")
            return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    logger.success("Database: Connected to DB")

    encoded_car = encode(car)

    metadata = {
        "_id": extract_id_from_link(car["link"]),
        "source": source,
        "scraper_version": scraper_version,
        "scrape_date": datetime.utcnow().isoformat(),
        "stage": "scrape",
    }

    if encoded_car is not None:
        encoded_car.update(metadata)

    result = conn[SCRAPE_COLLECTION].insert_one(encoded_car)
    return result.acknowledged


def update(client, link, new_fields, conn=None):
    try:
        conn = client.get_database(DATABASE)
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    try:
        result = conn[SCRAPE_COLLECTION].update_one(
            {"_id": extract_id_from_link(link)}, {"$set": new_fields}
        )
    except Exception as e:
        logger.error(f"Database: Failed to update car data. Error: {e}")
        return False

    return result.acknowledged


def update_listing_scores(client, cars_array, new_scores, model_number, model_version):
    logger.debug(f"Database: Bulk updating listing scores. new scores: {new_scores}")
    try:
        conn = client.get_database(DATABASE)
        if conn is not None:
            logger.error("Database: Failed to connect to DB.")
            return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    if len(cars_array) != len(new_scores):
        logger.critical(
            f"Database: Length of cars array ({len(cars_array)}) and scores array ({len(new_scores)}) do not match. Please fix your model :)"
        )
        return False

    if not cars_array:
        logger.warning("Database: No cars to update")
        return False

    if not new_scores:
        logger.warning("Database: No scores to update")
        return False

    if not model_version:
        logger.error("Database: No model version provided")
        return False

    if not model_number:
        logger.error("Database: No model number provided")
        return False

    try:
        update_operations = []
        for k, car in enumerate(cars_array):
            update_operation = UpdateOne(
                {"_id": car["_id"]},
                {
                    "$set": {
                        f"model_scores.model_{model_number}": new_scores[k],
                        f"model_versions.model_{model_number}": model_version,
                        "pending_risk_update": True
                    }
                },
            )
            update_operations.append(update_operation)

        if update_operations:
            result = conn[SCRAPE_COLLECTION].bulk_write(update_operations)
            return result.modified_count

    except Exception as e:
        logger.error(f"Database: Failed to update_all cars. Error: {e}")
        return False

    return True


def update_db_risk_scores(client, cars_array):
    logger.debug(f"Database: Bulk updating {len(cars_array)} risk scores.")
    try:
        conn = client.get_database(DATABASE)
        if conn is not None:
            logger.error("Database: Failed to connect to DB.")
            return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    if not cars_array:
        logger.warning("Database: No cars to update")
        return False

    try:
        update_operations = []
        for car in cars_array:
            update_operation = UpdateOne(
                {"_id": car["_id"]},
                {
                    "$set": {
                        "risk_score": car["risk_score"],
                        "pending_risk_update": False,
                        "human_flag": False
                    }
                },
            )
            update_operations.append(update_operation)

        if update_operations:
            result = conn[SCRAPE_COLLECTION].bulk_write(update_operations)
            return result.modified_count

    except Exception as e:
        logger.error(f"Database: Failed to update risk scores. Error: {e}")
        return False

    return 0


def find_pending_risk_update(client):
    try:
        conn = client.get_database(DATABASE)
        if conn is not None:
            logger.error("Database: Failed to connect to DB.")
            return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    try:
        return [decode(car) for car in conn[SCRAPE_COLLECTION].find({"pending_risk_update": True, "stage": "clean"})]
    except Exception as e:
        logger.error(f"Database: Failed to find cars pending a risk score update. Error: {e}")
        return None


def encode(obj):
    encoded_obj = {}

    try:
        for field, value in obj.items():
            if isinstance(value, str) and field not in DONT_DECODE:
                encoded_obj[field] = quote(value)
            elif (
                isinstance(value, list)
                and isinstance(value[0], str)
                and field not in DONT_DECODE
            ):
                encoded_obj[field] = encode_arr(value)
            else:
                encoded_obj[field] = value
    except Exception as e:
        logger.error(f"Database: Failed to encode object. Error: {e}")
        return None

    return encoded_obj


def decode(obj):
    decoded_obj = {}

    try:
        for field, value in obj.items():
            # the urls in the images field will not be decoded because they are an array
            if isinstance(value, str) and field not in DONT_DECODE:
                decoded_obj[field] = unquote(value)
            elif (
                isinstance(value, list)
                and isinstance(value[0], str)
                and field not in DONT_DECODE
            ):
                decoded_obj[field] = decode_arr(value)
            else:
                decoded_obj[field] = value
    except Exception as e:
        logger.error(f"Database: Failed to decode object. Error: {e}")
        return None

    return decoded_obj


def encode_arr(arr):
    encoded_arr = []

    try:
        for elem in arr:
            encoded_arr.append(quote(elem))
    except Exception as e:
        logger.error(f"Database: Failed to encode array. Error: {e}")
        return None

    return encoded_arr


def decode_arr(arr):
    decoded_arr = []

    try:
        for elem in arr:
            decoded_arr.append(unquote(elem))
    except Exception as e:
        logger.error(f"Database: Failed to decode array. Error: {e}")
        return None

    return decoded_arr


def __init__():
    logger.info("Database: Initialized")
