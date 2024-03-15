import os
import re
from datetime import date
from urllib.parse import quote, unquote

import pymongo
from dotenv import load_dotenv

DATABASE = "scrape"
COLLECTION = "scraped_raw"

DONT_DECODE = ["link", "_id", "price", "odometer"]


def get_conn(db):
    # load environment variable containing db uri
    # (which includes username and password)
    load_dotenv()

    # create a mongodb connection
    try:
        db_uri = os.environ.get("DB_URI")
        sanitized_uri = quote(db_uri)
        client = pymongo.MongoClient(sanitized_uri)

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

    return conn["db"][COLLECTION].find_one({"_id": extract_id_from_link(link)})


def find_cars_in_stage(stage):
    conn = get_conn(DATABASE)

    return [decode(car) for car in conn["db"][COLLECTION].find({"stage": stage})]


def find_all_cars():
    conn = get_conn(DATABASE)

    return conn["db"][COLLECTION].find()


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
    result = conn["db"][COLLECTION].insert_one(encoded_car)
    return result.acknowledged


def update(link, new_fields):
    conn = get_conn(DATABASE)
    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    result = conn["db"][COLLECTION].update_one(
        {"_id": extract_id_from_link(link)}, {"$set": new_fields}
    )
    return result.acknowledged


def encode(obj):
    encoded_obj = {}

    for field, value in obj.items():
        # the urls in the images field will not be encoded because they are an array
        if isinstance(value, str) and field not in DONT_DECODE:
            encoded_obj[field] = quote(value)
        elif isinstance(value, list) and field not in DONT_DECODE:
            encoded_obj[field] = encode_arr(field)
        else:
            encoded_obj[field] = value

    return encoded_obj


def decode(obj):
    decoded_obj = {}

    for field, value in obj.items():
        # the urls in the images field will not be decoded because they are an array
        if isinstance(value, str) and field not in DONT_DECODE:
            decoded_obj[field] = unquote(value)
        elif isinstance(value, list) and field not in DONT_DECODE:
            decoded_obj[field] = decode_arr(field)
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
