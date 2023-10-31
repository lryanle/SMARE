from dotenv import load_dotenv
import pymongo
import os
from datetime import date

def get_conn(db):
  # load environment variable containing db uri (which includes username and password)
  load_dotenv()
  db_uri = os.getenv("DB_URI")

  # create a mongodb connection
  try:
    client = pymongo.MongoClient(db_uri)
    
  # return a friendly error if a URI error is thrown 
  except pymongo.errors.ConfigurationError:
    print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string (found the .env)?")
    return {"success" : False, "db": 0}

  # use a database named "Test"
  return {"success" : True, "db": client.get_database(db)}

def post_raw(scraperVersion, source, title, price, location, miles, link, images = None, postBody = None, longitude = None, latitude = None, attributes = None):
  car = {
    "_id": link,
    "source": source,
    "scraper-version": scraperVersion,
    "scrape-date": str(date.today()),
    "title": title, 
    "price": price, 
    "location": location, 
    "odometer": miles, 
    "link": link
  }

  if (images is not None):
    car["images"] = images
  
  if (postBody is not None):
    car["postBody"] = postBody

  if (longitude is not None):
    car["longitude"] = longitude
  
  if (latitude is not None):
    car["latitude"] = latitude
  
  if (attributes is not None):
    for attr in attributes:
      car[attr["label"]] = attr["value"]

  # Insert into collection called "scrape_test"
  conn = get_conn("Test")

  if (conn["success"]):
    result = conn["db"]["raw"].insert_one(car)
    return result.acknowledged
  else:
    return False

def update(link, newFields):
  conn = get_conn("Test")
  if (conn["success"]):
    result = conn["db"]["raw"].update_one(
      {'_id': link},
      {
        '$set': newFields
      }
    )
    return result.acknowledged
  else:
    return False

