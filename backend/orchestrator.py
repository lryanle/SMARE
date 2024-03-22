from datetime import datetime, timedelta

from src.cleaners.cleaner import run as run_cleaner
from src.scrapers.scraper import run as run_scraper
from src.models.model_manager import run as run_analyzer
from src.utilities.logger import SmareLogger

SCRAPER_DURATION = 4 * 60
CLEANER_DURATION = 3 * 60
ANALYZER_DURATION = 4 * 60

CL_SCRAPER_VERSION = 5
FB_SCRAPER_VERSION = 5
CLEANER_VERSION = 1

DUPLICATE_TERMINATION_LIMIT = 5

logger = SmareLogger()


def calculate_timestamp(seconds):
    return datetime.now() + timedelta(seconds=seconds)


def facebook(termination_timestamp):
    logger.info(f"Running faceboook until {termination_timestamp}")
    run_scraper(termination_timestamp, "facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def craigslist(termination_timestamp):
    logger.info(f"Running craigslist until {termination_timestamp}")
    run_scraper(termination_timestamp, "craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def smare(scraper_name):
    if scraper_name == "facebook":
        logger.info("Starting SMARE with facebook...")
        scraper = facebook
    elif scraper_name == "craigslist":
        logger.info("Starting SMARE with craigslist...")
        scraper = craigslist

    # scraper(calculate_timestamp(SCRAPER_DURATION))
    run_cleaner(calculate_timestamp(SCRAPER_DURATION), CLEANER_VERSION)
    # run_analyzer(calculate_timestamp(ANALYZER_DURATION))


def smare_cragigslist():
    smare("craigslist")


def smare_facebook():
    smare("facebook")


if __name__ == "__main__":
    smare_facebook()
    # smare_cragigslist()
