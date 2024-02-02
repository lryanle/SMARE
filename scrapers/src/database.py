import os
from datetime import date
import re
from urllib.parse import quote, unquote

import pymongo
from dotenv import load_dotenv

db = "scrape"
collection = "scraped_raw"


def get_conn(db):
    # load environment variable containing db uri (which includes username and password)
    load_dotenv()
    db_uri = os.environ.get("DB_URI")

    # create a mongodb connection
    try:
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
    facebook = re.search(r'facebook\.com/marketplace/item/(\d+)/', link)
    craigslist = re.search(r'/(\d+)\.html$', link)

    if facebook:
        return facebook.group(1)
    elif craigslist:
        return craigslist.group(1)
    else:
        raise Exception("Not a valid Craigslist nor Facebook link")


def find_post_with_link(link):
    conn = get_conn(db)

    return conn["db"][collection].find_one({"_id": extract_id_from_link(link)})


def post_raw(
    scraperVersion,
    source,
    title,
    price,
    location,
    miles,
    link,
    images=None,
    postBody=None,
    longitude=None,
    latitude=None,
    attributes=None,
):
    car = {
        "_id": link,
        "source": source,
        "scraper-version": scraperVersion,
        "scrape-date": str(date.today()),
        "title": title,
        "price": price,
        "location": location,
        "odometer": miles,
        "link": link,
    }

    if images is not None:
        car["images"] = images

    if postBody is not None:
        car["postBody"] = postBody

    if longitude is not None:
        car["longitude"] = longitude

    if latitude is not None:
        car["latitude"] = latitude

    if attributes is not None:
        for attr in attributes:
            car[attr["label"]] = attr["value"]

    print("Connecting to DB...")

    # Insert into collection called "scraped_raw"
    conn = get_conn(db)

    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    print("Connected to DB")

    result = conn["db"][collection].insert_one(encode(car))
    return result.acknowledged


def update(link, newFields):
    conn = get_conn(db)
    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    result = conn["db"][collection].update_one({"_id": link}, {"$set": newFields})
    return result.acknowledged


def encode(obj):
    encodedObj = {}

    for field, value in obj.items():
        if isinstance(value, str):
            encodedObj[field] = quote(value)
        else:
            encodedObj[field] = value

    return encodedObj


def decode(obj):
    decodedObj = {}

    for field, value in obj.items():
        if isinstance(value, str):
            decodedObj[field] = unquote(value)
        else:
            decodedObj[field] = value

    return decodedObj
