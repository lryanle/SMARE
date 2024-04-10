import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from src.cleaners.cleaner import run as run_cleaner
from src.models.model_manager import run as run_analyzer
from src.scrapers.scraper import run as run_scraper
from src.utilities.logger import SmareLogger

load_dotenv()

SCRAPER_DURATION = int(os.environ.get("SCRAPE_MINUTES", 6)) * 60
CLEANER_DURATION = int(os.environ.get("CLEAN_MINUTES", 2)) * 60
ANALYZER_DURATION = int(os.environ.get("ANALYZE_MINUTES", 4)) * 60

CL_SCRAPER_VERSION = 6
FB_SCRAPER_VERSION = 6
CLEANER_VERSION = 3

logger = SmareLogger()


def calculate_timestamp(seconds):
    try:
        return datetime.now() + timedelta(seconds=seconds)
    except Exception as e:
        logger.critical(f"Orchestrator failed to generate module termination-timestamp. Error: {e}")


def facebook(termination_timestamp):
    try:
        run_scraper(termination_timestamp, "facebook", FB_SCRAPER_VERSION)
    except Exception as e:
        logger.critical(f"Orchestrator failed runnning facebook scraper. Error: {e}")


def craigslist(termination_timestamp):
    try:
        run_scraper(termination_timestamp, "craigslist", CL_SCRAPER_VERSION)
    except Exception as e:
        logger.critical(f"Orchestrator failed runnning craigslist scraper. Error: {e}")


def smare(scraper_name):
    try:
        if scraper_name == "facebook":
            logger.info("Starting SMARE with facebook...")
            scraper = facebook
        elif scraper_name == "craigslist":
            logger.info("Starting SMARE with craigslist...")
            scraper = craigslist
        else:
            logger.critical(f"Invalid scraper name specified '{scraper_name}'")
            return None

        scraper(calculate_timestamp(SCRAPER_DURATION))
    except Exception as e:
        logger.critical(f"Orchestrator failed while runnning the scraper module. Error: {e}")

    try:
        run_cleaner(calculate_timestamp(SCRAPER_DURATION), CLEANER_VERSION)
    except Exception as e:
        logger.critical(f"Orchestrator failed runnning the cleaner module. Error: {e}")

    try:
        run_analyzer(calculate_timestamp(ANALYZER_DURATION))
    except Exception as e:
        logger.critical(f"Orchestrator failed runnning analyzer module (model manager). Error: {e}")

# event and context are needed to work in AWS lambda
def smare_craigslist(event="", context=""):
    try:
        logger.debug("Attempting to start SMARE with Craigslist scraper")
        smare("craigslist")
    except Exception as e:
        logger.critical(f"SMARE failed running the craigslist pipeline. Error: {e}")


# event and context are needed to work in AWS lambda
def smare_facebook(event="", context=""):
    try:
        logger.debug("Attempting to start SMARE with Facebook scraper")
        smare("facebook")
    except Exception as e:
        logger.critical(f"SMARE failed running the facebook pipeline. Error: {e}")
