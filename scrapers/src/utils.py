from selenium import webdriver
from pymongo.errors import DuplicateKeyError

from . import craigslist
from . import database as db
from . import facebook


def scrollTo(x, driver):
    driver.execute_script(
        f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})"
    )


def clickOn(elem, driver):
    driver.execute_script("arguments[0].click();", elem)


def createDriverOptions():
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


def setupBrowser():
    print("Setting up headless browser")

    service = webdriver.ChromeService("/opt/chromedriver")
    options = createDriverOptions()

    print("Creating a new Selenium WebDriver instance")
    return webdriver.Chrome(options=options, service=service)


def scrape(website, scraperVersion, duplicateThreshold):
    if website == "craigslist":
        scraper = craigslist
    elif website == "facebook":
        scraper = facebook

    cityURLs = scraper.setupURLs(2011)
    browser = setupBrowser()

    for url in cityURLs:
        print(f"Going to {url}")
        browser.get(url)

        print(f"Loading cars from {url}")
        scraper.loadPageResources(browser)

        carPosts = scraper.getAllPosts(browser)

        duplicatePostCount = 0

        for post in carPosts:
            if (duplicatePostCount >= duplicateThreshold):
                print(f"Reached duplicate threshold of {duplicateThreshold}")
                break

            try:
                title, price, location, odometer, link, images = scraper.getCarInfo(
                    post
                )
                success = db.post_raw(
                    scraperVersion,
                    website,
                    title,
                    price,
                    location,
                    odometer,
                    link,
                    images,
                )
                if success:
                    print("posted to db")
                else:
                    print("failed to post to db")
            except DuplicateKeyError:
                duplicatePostCount += 1
                print(f"Duplicate post found ({duplicatePostCount} / {duplicateThreshold})")
            except Exception as error:
                print(error)

    browser.quit()
