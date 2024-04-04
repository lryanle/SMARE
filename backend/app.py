from orchestrator import smare_cragigslist, smare_facebook, CL_SCRAPER_VERSION, FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT, CLEANER_VERSION
from src.cleaners import cleaner
from src.scrapers import scraper
from src.models import model_manager

from datetime import datetime, timedelta

TERMINATION_TIMESTAMP = datetime.now() + timedelta(days=7)


def pipeline_facebook():
    smare_facebook()


def pipeline_craigslist():
    smare_cragigslist()


def craigslist():
    scraper.run(TERMINATION_TIMESTAMP, "craigslist", CL_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def facebook():
    scraper.run(TERMINATION_TIMESTAMP, "facebook", FB_SCRAPER_VERSION, DUPLICATE_TERMINATION_LIMIT)


def clean():
    cleaner.run(TERMINATION_TIMESTAMP, CLEANER_VERSION)


def model():
    model_manager.run(TERMINATION_TIMESTAMP)
