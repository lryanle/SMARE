from src.scrapers import scraper
from src.cleaners import cleaner

CL_SCRAPER_VERSION = 5
FB_SCRAPER_VERSION = 5
CLEANER_VERSION = 1

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
    scraper.run("craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def facebook():
    scraper.run("facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def clean():
    logs, loggerFactory = initializeLogger()

    cleaner.run(loggerFactory("clean"), False, CLEANER_VERSION)

    print(logs)
