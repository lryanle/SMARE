import json
import os

import pymongo
from dotenv import load_dotenv
from loguru import logger


def mongo_sink(self):
    def sink_function(record):
        record = json.loads(record)
        rec = record["record"]

        post_log(
            self.db_conn,
            rec["time"]["repr"],
            rec["level"]["name"],
            rec["message"],
            rec["file"]["name"],
            rec["file"]["path"],
            rec["line"],
            rec["name"],
            rec["module"],
            rec["extra"]["source"] if "source" in rec["extra"] else None,
            (
                rec["exception"]["type"]
                if rec["exception"] and "type" in rec["exception"]
                else None
            ),
            (
                record["text"]
                if rec["exception"] and "type" in rec["exception"]
                else None
            ),
        )

    return sink_function


DATABASE = "scrape"
LOG_COLLECTION = "logs"


def get_conn(db=DATABASE):
    # load environment variable containing db uri
    # (which includes username and password)
    try:
        load_dotenv()
    except Exception as e:
        print(f"Logger: Failed to load .env file. Error: {e}")
        return {"success": False, "db": 0}

    # create a mongodb connection
    try:
        db_uri = os.environ.get("DB_URI")
        # deepcode ignore Ssrf: .env's content is controlled by the developer
        client = pymongo.MongoClient(db_uri)

    # return a friendly error if a URI error is thrown
    except pymongo.errors.ConfigurationError:
        print(
            "Logger: "
            "An Invalid URI host error was received."
            " Is your Atlas host name correct in your connection string (found the .env)?"
        )
        return {"success": False, "db": 0}

    return {"success": True, "db": client.get_database(db)}


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
        print(f"Database: Failed to post log to the db. Error: {e}")
        return False

    return result.acknowledged


class SmareLogger:
    def __init__(self):
        logger.add("logs/log_{time}.log", rotation="12:00", compression="zip")

        self.db_conn = get_conn()
        if not self.db_conn["success"]:
            logger.critical("Logger failed to connect to the MongoDB database.")
            raise ConnectionError("Failed to connect to the MongoDB database.")

        logger.add(
            mongo_sink(self),
            serialize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            filter=(lambda record: record["level"].no >= 30),
        )

    # -----------------------------------------------

    def debug(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).debug(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")

    def info(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).info(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")

    def success(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).success(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")

    def warning(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).warning(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")

    def error(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).error(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")

    def critical(self, message, source=None):
        try:
            msg = f"{source}: {message}" if source else message

            logger.bind(source=source).critical(msg)
        except Exception as e:
            logger.critical(f"Error: {e}")
