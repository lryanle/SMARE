import os
import re
from datetime import date
from urllib.parse import quote, unquote

import pymongo
from dotenv import load_dotenv

from .logger import SmareLogger

DATABASE = "scrape"
SCRAPE_COLLECTION = "listings"
LOG_COLLECTION = "logs"

DONT_DECODE = ["link", "_id", "price", "odometer", "images"]

logger = SmareLogger()


def get_conn(db=DATABASE):
    # load environment variable containing db uri
    # (which includes username and password)
    try:
        load_dotenv()
    except Exception as e:
        logger.critical(f"Database: Failed to load .env file. Error: {e}")
        return {"success": False, "db": 0}

    # create a mongodb connection
    try:
        db_uri = os.environ.get("DB_URI")
        # deepcode ignore Ssrf: .env's content is controlled by the developer
        client = pymongo.MongoClient(db_uri)

    # return a friendly error if a URI error is thrown
    except pymongo.errors.ConfigurationError:
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


def find_post_with_link(link):
    try:
        conn = get_conn(DATABASE)

        return conn["db"][SCRAPE_COLLECTION].find_one(
            {"_id": extract_id_from_link(link)}
        )
    except Exception as e:
        logger.error(f"Database: Failed to find post with link. Error: {e}")
        return None


def find_cars_in_stage(stage):
    try:
        conn = get_conn(DATABASE)

        return [
            decode(car) for car in conn["db"][SCRAPE_COLLECTION].find({"stage": stage})
        ]
    except Exception as e:
        logger.error(f"Database: Failed to find cars in stage. Error: {e}")
        return None


def find_all_cars():
    try:
        conn = get_conn(DATABASE)

        return conn["db"][SCRAPE_COLLECTION].find()
    except Exception as e:
        logger.error(f"Database: Failed to find all cars. Error: {e}")
        return None


def find_unanalyzed_cars(current_versions):
    try:
        conn = get_conn(DATABASE)

        query = {
            "stage": "clean",
            "$or": [
                {"$or": [
                    {"model_scores.model_1": -1},
                    {"model_scores.model_2": -1},
                    {"model_scores.model_3": -1},
                    {"model_scores.model_4": -1},
                    {"model_scores.model_5": -1},
                    {"model_scores.model_6": -1},
                    {"model_scores.model_7": -1},
                ]},
                {"$or": [
                    {"model_versions.model_1": {"$not": {"$eq": current_versions[0]}}},
                    {"model_versions.model_2": {"$not": {"$eq": current_versions[1]}}},
                    {"model_versions.model_3": {"$not": {"$eq": current_versions[2]}}},
                    {"model_versions.model_4": {"$not": {"$eq": current_versions[3]}}},
                    {"model_versions.model_5": {"$not": {"$eq": current_versions[4]}}},
                    {"model_versions.model_6": {"$not": {"$eq": current_versions[5]}}},
                    {"model_versions.model_7": {"$not": {"$eq": current_versions[6]}}},
                ]}
            ],
        }

        return [decode(car) for car in conn["db"][SCRAPE_COLLECTION].find(query)]
    except Exception as e:
        logger.error(f"Database: Failed to find unanalyzed cars. Error: {e}")
        return None


def post_raw(scraper_version, source, car):
    logger.info("Database: Connecting to DB...")
    try:
        conn = get_conn(DATABASE)
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    if not conn["success"]:
        logger.error("Database (post_raw): Failed to connect to DB.")
        return False

    logger.success("Database: Connected to DB")

    # Encode car listing
    encoded_car = encode(car)

    metadata = {
        "_id": extract_id_from_link(car["link"]),
        "source": source,
        "scraper_version": scraper_version,
        "scrape_date": str(date.today()),
        "stage": "scrape",
    }

    # attach metadata to car before pushing to db
    if encoded_car is not None:
        encoded_car.update(metadata)

        try:
            # push encoded car (with metadata) to db
            result = conn["db"][SCRAPE_COLLECTION].insert_one(encoded_car)
            return result.acknowledged
        except Exception as e:
            logger.error(f"Database: Failed to post raw car data to the db. Error: {e}")
            return False


def update(link, new_fields, conn=None):
    try:
        if conn is None:
            conn = get_conn(DATABASE)

            if not conn["success"]:
                logger.error("Database: Failed to connect to DB.")
                return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    try:
        result = conn["db"][SCRAPE_COLLECTION].update_one(
            {"_id": extract_id_from_link(link)}, {"$set": new_fields}
        )
    except Exception as e:
        logger.error(f"Database: Failed to update car data. Error: {e}")
        return False

    return result.acknowledged


def update_listing_scores(cars_array, new_scores, model_number, model_version):
    logger.debug(f"Database: Bulk updating listing scores. new scores: {new_scores}")
    try:
        conn = get_conn(DATABASE)
        if not conn["success"]:
            logger.error("Database: Failed to connect to DB.")
            return False
    except Exception as e:
        logger.error(f"Database: Failed to connect to DB. Error: {e}")
        return False

    if len(cars_array) != len(new_scores):
        logger.critical(
            "Database: Length of cars array and scores array do not match. Please fix your model :)"
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
            model_field_score = f"model_scores.model_{model_number}"
            model_field_version = f"model_versions.model_{model_number}"

            update_operation = update_one(
                {"_id": car["_id"]},
                {
                    "$set": {
                        model_field_score: new_scores[k],
                        model_field_version: model_version,
                    }
                },
            )
            update_operations.append(update_operation)

        if update_operations:
            result = conn["db"][SCRAPE_COLLECTION].bulk_write(update_operations)
            return result.modified_count

    except Exception as e:
        logger.error(f"Database: Failed to update_all cars. Error: {e}")
        return False

    return True


def post_log(
    conn,
    time,
    level,
    message,
    file_name,
    file_path,
    line_number,
    function_name,
    function_module,
    source=None,
    exception=None,
    long_message=None,
):
    log = {
        "date": time,
        "level": level,
        "message": message,
        "file_name": file_name,
        "file_path": file_path,
        "line_number": line_number,
        "function_name": function_name,
        "function_module": function_module,
        "source": source,
        "exception": exception,
        "long_message": long_message,
    }

    try:
        result = conn["db"][LOG_COLLECTION].insert_one(log)
    except Exception as e:
        logger.error(f"Database: Failed to post log to the db. Error: {e}")
        return False

    return result.acknowledged


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
