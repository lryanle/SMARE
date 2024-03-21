from src.cleaners import cleaner
from src.scrapers import scraper

CL_SCRAPER_VERSION = 5
FB_SCRAPER_VERSION = 5
CLEANER_VERSION = 1

DUPLICATE_TERMINATION_LIMIT = 5


def craigslist():
    scraper.run(False, "craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def facebook():
    scraper.run(False, "facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def clean():
    cleaner.run(False, CLEANER_VERSION)
