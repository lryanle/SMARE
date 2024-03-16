from pymongo.errors import DuplicateKeyError

from ..utilities import database as db
from ..utilities import logger
from . import craigslist, facebook
from .utils import load_page_resources, setup_browser

logger = logger.SmareLogger()


def run(website, scraper_version, duplicate_threshold):
    logger.info(f"Starting {website} scraper...")

    if website == "craigslist":
        scraper = craigslist
    elif website == "facebook":
        scraper = facebook

    city_urls = scraper.setup_urls(2011)
    browser = setup_browser()

    for url in city_urls:
        logger.debug(f"Going to {url}")
        browser.get(url)

        logger.debug(f"Loading cars from {url}")
        load_page_resources(browser)

        car_posts = scraper.get_all_posts(browser)

        duplicate_post_count = 0

        for post in car_posts:
            if duplicate_post_count >= duplicate_threshold:
                logger.warning(f"Reached duplicate threshold of {duplicate_threshold}")
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
                    f"Duplicate post found ({duplicate_post_count} / {duplicate_threshold})"
                )
            except Exception as error:
                logger.error(f"Encountered an error: {error}")

    logger.success(f"Finished {website} scraper")
    browser.quit()
