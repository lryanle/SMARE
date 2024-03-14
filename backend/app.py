from src.scrapers import utils as scrapeUtil
from src.cleaners import cleaner

CL_SCRAPER_VERSION = 4
FB_SCRAPER_VERSION = 4

DUPLICATE_TERMINATION_LIMIT = 5


def initializeLogger():
    log = {
        "scrape": [],
        "clean": [],
        "analyze": []
    }

    def loggerFactory(module):
        def logger(message):
            log[module].append(message)

        return logger

    return log, loggerFactory


def craigslist():
    scrapeUtil.scrape("craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def facebook():
    scrapeUtil.scrape("facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def clean():
    logs, loggerFactory = initializeLogger()

    cleaner.run(loggerFactory("clean"), False)

    print(logs)
