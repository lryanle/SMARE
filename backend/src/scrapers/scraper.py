from pymongo.errors import DuplicateKeyError

from .. import database as db
from . import craigslist, facebook
from .utils import load_page_resources, setup_browser


def run(website, scraper_version, duplicate_threshold):
    if website == "craigslist":
        website = craigslist
    elif website == "facebook":
        website = facebook

    city_urls = website.setup_urls(2011)
    browser = setup_browser()

    for url in city_urls:
        print(f"Going to {url}")
        browser.get(url)

        print(f"Loading cars from {url}")
        load_page_resources(browser)

        car_posts = website.get_all_posts(browser)

        duplicate_post_count = 0

        for post in car_posts:
            if duplicate_post_count >= duplicate_threshold:
                print(f"Reached duplicate threshold of {duplicate_threshold}")
                break

            try:
                post = website.get_car_info(post)
                stage2 = website.scrape_listing(post["link"], browser)

                post.update(stage2)

                success = db.postRaw(scraper_version, website, post)
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
