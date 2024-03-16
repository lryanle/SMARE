from pymongo.errors import DuplicateKeyError

from ..utilities import database as db
from . import craigslist, facebook
from .utils import load_page_resources, setup_browser


def run(website, scraper_version, duplicate_threshold):
    if website == "craigslist":
        scraper = craigslist
    elif website == "facebook":
        scraper = facebook

    city_urls = scraper.setup_urls(2011)
    browser = setup_browser()

    for url in city_urls:
        print(f"Going to {url}")
        browser.get(url)

        print(f"Loading cars from {url}")
        load_page_resources(browser)

        car_posts = scraper.get_all_posts(browser)

        duplicate_post_count = 0

        for post in car_posts:
            if duplicate_post_count >= duplicate_threshold:
                print(f"Reached duplicate threshold of {duplicate_threshold}")
                break

            try:
                post = scraper.get_car_info(post)
                stage2 = scraper.scrape_listing(post["link"], browser)

                post.update(stage2)

                success = db.post_raw(scraper_version, website, post)
                if success:
                    print("posted to db")
                else:
                    print("failed to post to db")
            except DuplicateKeyError:
                duplicate_post_count += 1
                print(
                    f"Duplicate post found ({duplicate_post_count} / {duplicate_threshold})"
                )
            except Exception as error:
                print(error)

    browser.quit()
