import os
from datetime import datetime

from pymongo.errors import DuplicateKeyError

from ..utilities import database as db
from ..utilities import logger
from . import craigslist, facebook
from .utils import load_page_resources, setup_browser

DUP_LIMIT = int(os.environ.get("SCRAPE_DUP_LIMIT", 5))

logger = logger.SmareLogger()


def run(termination_timestamp, website, scraper_version):
    logger.info(f"Starting {website} scraper...")

    if website == "craigslist":
        scraper = craigslist
        is_proxy_enabled = False
    elif website == "facebook":
        scraper = facebook
        is_proxy_enabled = os.environ.get("PROD_ENV", False) # true only in production
    else:
        logger.critical(f"Unsuported website! '{website}'")
        return None

    city_urls = scraper.setup_urls(2011)
    browser = setup_browser(is_proxy_enabled)

    for url in city_urls:
        if datetime.now() >= termination_timestamp:
                logger.info("Scraping process is done.")
                break

        logger.debug(f"Going to {url}")
        browser.get(url)

        logger.debug(f"Loading cars from {url}")
        load_page_resources(browser)

        car_posts = scraper.get_all_posts(browser)
        if not car_posts:
            logger.warning(f"No posts found in {url}")

        logger.info(f"Found {len(car_posts)} in {url}")

        duplicate_post_count = 0

        for post in car_posts:
            if datetime.now() >= termination_timestamp:
                logger.info("Scraping process is done.")
                break

            if duplicate_post_count >= DUP_LIMIT:
                logger.warning(f"Reached duplicate threshold of {DUP_LIMIT}")
                break

            try:
                post = scraper.get_car_info(post)
                stage2 = scraper.scrape_listing(post["link"], browser)

                post.update(stage2)

                success = db.post_raw(scraper_version, website, post)
                if success:
                    logger.success("Posted to db")
                else:
                    logger.error("Failed to post to db")
            except DuplicateKeyError:
                duplicate_post_count += 1
                logger.warning(
                    f"Duplicate post found ({duplicate_post_count} / {DUP_LIMIT})"
                )
            except Exception as error:
                logger.error(f"Encountered an error: {error}")

    logger.success(f"Finished {website} scraper")
    browser.quit()
