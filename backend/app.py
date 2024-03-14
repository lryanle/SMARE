from src.scrapers import utils as scrapeUtil
from src.cleaners import cleaner

CL_SCRAPER_VERSION = 4
FB_SCRAPER_VERSION = 4

DUPLICATE_TERMINATION_LIMIT = 5


def craigslist():
    scrapeUtil.scrape("craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def facebook():
    scrapeUtil.scrape("facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def clean():
    logs = {}
    cleaner.run(logs, False)
