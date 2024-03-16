import json
from loguru import logger
from database import get_conn, post_log


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