import datetime
import sys
from loguru import logger
from database import get_conn, post_raw, post_log

def mongo_sink(self, level):
  def sink_function(record):
    if record["level"].name == level:
      timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      post_log(self.db_conn["db"], timestamp, record["message"], level)
  return sink_function

class CustomLogger:
  def __init__(self):
    self.db_conn = get_conn()
    if not self.db_conn["success"]:
      logger.critical("Logger failed to connect to the MongoDB database.")
      raise ConnectionError("Failed to connect to the MongoDB database.")
    
  def log_to_file(self, message, level):
    logger.add("log_{time}.log", "{time} - {level} - {message}", level, rotation="12:00", compression="zip")

  def log_to_mongo(self, message, level):
    if self.db_conn["success"]:
      logger.add(mongo_sink(self, level), "{time} - {level} - {message}", level, serialize=True, backtrace=True, diagnose=True, enqueue=True) # todo: add source to log if provided
      

  def debug(self, message, source=None):
    # todo: add source to log if provided
    if source:
      logger.bind(source).debug(f"{source}: {message}")
    else:
      logger.debug(message)

  def info(self, message, source=None):
    # todo: add source to log if provided
    logger.info(message)

  def success(self, message, source=None):
    # todo: add source to log if provided
    logger.success(message)

  def warning(self, message, source=None):
    # todo: add source to log if provided
    logger.warning(message)
    self.log_to_mongo(message, "WARNING")

  def error(self, message, source=None):
    # todo: add source to log if provided
    logger.error(message)
    self.log_to_mongo(message, "ERROR")

  def critical(self, message, source=None):
    # todo: add source to log if provided
    logger.critical(message)
    self.log_to_mongo(message, "CRITICAL")


# Usage example
custom_logger = CustomLogger()
custom_logger.info("Server started successfully")
custom_logger.error("Failed to connect to the database")
