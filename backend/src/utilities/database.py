import os
import re
from datetime import date
from urllib.parse import quote, unquote

import pymongo
from dotenv import load_dotenv

DATABASE = "scrape"
SCRAPE_COLLECTION = "scraped_raw"
LOG_COLLECTION = "logs"

DONT_DECODE = ["link", "_id", "price", "odometer", "images"]


def get_conn(db=DATABASE):
    # load environment variable containing db uri
    # (which includes username and password)
    load_dotenv()

    # create a mongodb connection
    try:
        db_uri = os.environ.get("DB_URI")
        # deepcode ignore Ssrf: .env's content is controlled by the developer
        client = pymongo.MongoClient(db_uri)

    # return a friendly error if a URI error is thrown
    except pymongo.errors.ConfigurationError:
        print(
            "An Invalid URI host error was received."
            " Is your Atlas host name correct in your connection string (found the .env)?"
        )
        return {"success": False, "db": 0}

    return {"success": True, "db": client.get_database(db)}


def extract_id_from_link(link):
    facebook = re.search(r"facebook\.com/marketplace/item/(\d+)/", link)
    craigslist = re.search(r"/(\d+)\.html$", link)

    if facebook:
        return facebook.group(1)

    if craigslist:
        return craigslist.group(1)


def find_post_with_link(link):
    conn = get_conn(DATABASE)

    return conn["db"][SCRAPE_COLLECTION].find_one({"_id": extract_id_from_link(link)})


def find_cars_in_stage(stage):
    conn = get_conn(DATABASE)

    return [decode(car) for car in conn["db"][SCRAPE_COLLECTION].find({"stage": stage})]


def find_all_cars():
    conn = get_conn(DATABASE)

    return conn["db"][SCRAPE_COLLECTION].find()


def find_unanalyzed_cars(model):
    conn = get_conn(DATABASE)

    return [decode(car) for car in conn["db"][SCRAPE_COLLECTION].find({"stage": "clean", model: -1})]


def post_raw(scraper_version, source, car):
    print("Connecting to DB...")
    conn = get_conn(DATABASE)

    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    print("Connected to DB")

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
    encoded_car.update(metadata)

    # push encoded car (with metadata) to db
    result = conn["db"][SCRAPE_COLLECTION].insert_one(encoded_car)
    return result.acknowledged


def update(link, new_fields):
    conn = get_conn(DATABASE)
    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    result = conn["db"][SCRAPE_COLLECTION].update_one(
        {"_id": extract_id_from_link(link)}, {"$set": new_fields}
    )
    return result.acknowledged


def post_log(conn, time, level, message, file_name, file_path, line_number, function_name, function_module, source=None, exception=None, long_message=None):
    log = {"date": time, "level": level, "message": message, "file_name": file_name, "file_path": file_path,
           "line_number": line_number, "function_name": function_name, "function_module": function_module, "source": source, "exception": exception, "long_message": long_message}

    result = conn["db"][LOG_COLLECTION].insert_one(log)
    return result.acknowledged


def encode(obj):
    encoded_obj = {}

    for field, value in obj.items():
        if isinstance(value, str) and field not in DONT_DECODE:
            encoded_obj[field] = quote(value)
        elif isinstance(value, list) and isinstance(value[0], str) and field not in DONT_DECODE:
            encoded_obj[field] = encode_arr(value)
        else:
            encoded_obj[field] = value

    return encoded_obj


def decode(obj):
    decoded_obj = {}

    for field, value in obj.items():
        # the urls in the images field will not be decoded because they are an array
        if isinstance(value, str) and field not in DONT_DECODE:
            decoded_obj[field] = unquote(value)
        elif isinstance(value, list) and isinstance(value[0], str) and field not in DONT_DECODE:
            decoded_obj[field] = decode_arr(value)
        else:
            decoded_obj[field] = value

    return decoded_obj


def encode_arr(arr):
    encoded_arr = []

    for elem in arr:
        encoded_arr.append(quote(elem))

    return encoded_arr


def decode_arr(arr):
    decoded_arr = []

    for elem in arr:
        decoded_arr.append(unquote(elem))

    return decoded_arr


def __init__():
    print("database initialized")
