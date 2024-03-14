import time

from pymongo.errors import DuplicateKeyError
from selenium import webdriver

from .. import database as db
from . import craigslist, facebook


def scroll_to(x, driver):
    driver.execute_script(
        f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})"
    )


def click_on(elem, driver):
    driver.execute_script("arguments[0].click();", elem)


def create_driver_options():
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/chrome/chrome"

    options.add_argument("--headless=new")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")

    return options


def setup_browser():
    print("Setting up headless browser")

    service = webdriver.ChromeService("/opt/chromedriver")
    options = create_driver_options()

    print("Creating a new Selenium WebDriver instance")
    return webdriver.Chrome(options=options, service=service)


def load_page_resources(driver):
    scroll = 1000

    print("Waiting to load...")
    time.sleep(2)
    scroll_to(scroll, driver)
    time.sleep(2)


def scrape(website, scraper_version, duplicate_threshold):
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
