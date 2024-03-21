import multiprocessing
import time

from src.cleaners.cleaner import run as run_cleaner
from src.scrapers.scraper import run as run_scraper
from src.models.model_manager import run as run_analyzer
from src.utilities.logger import SmareLogger

logger = SmareLogger()


def timer(duration):
    time.sleep(duration)


def runModule(duration, target, version):
    done = multiprocessing.Value("b", False)

    mod = multiprocessing.Process(target=target, args=(done, version))
    mod.start()

    # wait for duration, then stop the module
    logger.debug(f"starting timer for {duration} seconds")
    timer(duration)
    done.value = True
    logger.debug("timer finished, set process boolean flag to true")

    # wait until the module process returns
    mod.join()
    logger.debug("process completed")


def facebook(is_done):
    run_scraper(is_done, "facebook", 5, 5)


def craigslist(is_done):
    run_scraper(is_done, "craigslist", 5, 5)


def cleaner(is_done):
    run_scraper(is_done, 1)


def model_manager(is_done):
    run_analyzer(is_done)

if __name__ == "__main__":
    logger.info("Starting SMARE...")
    runModule(20, facebook)
    # runModule(20, craigslist)
    runModule(20, cleaner)
    # runModule(20, model_manager)
