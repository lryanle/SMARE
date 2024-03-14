import os
import re
from datetime import date
from urllib.parse import quote, unquote

import pymongo
from dotenv import load_dotenv

DATABASE = "scrape"
COLLECTION = "scraped_raw"


def getConn(db):
    # load environment variable containing db uri
    # (which includes username and password)
    load_dotenv()
    dbURI = os.environ.get("DB_URI")

    # create a mongodb connection
    try:
        client = pymongo.MongoClient(dbURI)

    # return a friendly error if a URI error is thrown
    except pymongo.errors.ConfigurationError:
        print(
            "An Invalid URI host error was received."
            " Is your Atlas host name correct in your connection string (found the .env)?"
        )
        return {"success": False, "db": 0}

    return {"success": True, "db": client.get_database(db)}


def extractIdFromLink(link):
    facebook = re.search(r"facebook\.com/marketplace/item/(\d+)/", link)
    craigslist = re.search(r"/(\d+)\.html$", link)

    if facebook:
        return facebook.group(1)

    if craigslist:
        return craigslist.group(1)


def findPostWithLink(link):
    conn = getConn(DATABASE)

    return conn["db"][COLLECTION].find_one({"_id": extractIdFromLink(link)})


def findCarsInStage(stage):
    conn = getConn(DATABASE)

    return conn["db"][COLLECTION].find({"stage": stage})


def findAllCars():
    conn = getConn(DATABASE)

    return conn["db"][COLLECTION].find()


def postRaw(scraperVersion, source, car):
    print("Connecting to DB...")
    conn = getConn(DATABASE)

    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    print("Connected to DB")

    # Encode car listing
    encodedCar = encode(car)
    if source == "facebook":
        encodedCar["attributes"] = encodeArr(encodedCar["attributes"])

    metadata = {
        "_id": extractIdFromLink(car["link"]),
        "source": source,
        "scraper-version": scraperVersion,
        "scrape-date": str(date.today()),
        "stage": "scrape"
    }

    # attach metadata to car before pushing to db
    encodedCar.update(metadata)

    # push encoded car (with metadata) to db
    result = conn["db"][COLLECTION].insert_one(encodedCar)
    return result.acknowledged


def update(link, newFields):
    conn = getConn(DATABASE)
    if not conn["success"]:
        print("Failed to connect to DB...")
        return False

    result = conn["db"][COLLECTION].update_one(
        {"_id": extractIdFromLink(link)}, {"$set": newFields}
    )
    return result.acknowledged


def encode(obj):
    encodedObj = {}

    for field, value in obj.items():
        # the urls in the images field will not be encoded because they are an array
        if isinstance(value, str) and field != "link":
            encodedObj[field] = quote(value)
        else:
            encodedObj[field] = value

    return encodedObj


def decode(obj):
    decodedObj = {}

    for field, value in obj.items():
        # the urls in the images field will not be decoded because they are an array
        if isinstance(value, str) and field != "link":
            decodedObj[field] = unquote(value)
        else:
            decodedObj[field] = value

    return decodedObj


def encodeArr(arr):
    encodedArr = []

    for elem in arr:
        encodedArr.append(quote(elem))

    return encodedArr


def deencodeArr(arr):
    dencodedArr = []

    for elem in arr:
        dencodedArr.append(unquote(elem))

    return dencodedArr
