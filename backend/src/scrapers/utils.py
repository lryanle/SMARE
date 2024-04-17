import os
import time

from selenium import webdriver

from ..utilities import logger
from .extension import proxies

logger = logger.SmareLogger()

def scroll_to(x, driver):
    driver.execute_script(
        f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})"
    )


def click_on(elem, driver):
    driver.execute_script("arguments[0].click();", elem)


def create_driver_options(use_proxy=False):
    options = webdriver.ChromeOptions()
    options.binary_location = "/opt/chrome/chrome"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")

    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    if use_proxy:
        logger.info("Setting up proxy")

        username = os.getenv("PROXY_USERNAME")
        password = os.getenv("PROXY_PASSWORD")
        port = os.getenv("PROXY_PORT")
        ENDPOINT = 'gate.smartproxy.com'

        proxies_extension = proxies(username, password, ENDPOINT, port)
        options.add_extension(proxies_extension)

    return options


def setup_browser(use_proxy=False):
    logger.info("Setting up headless browser")

    service = webdriver.ChromeService("/opt/chromedriver")
    options = create_driver_options(use_proxy)

    logger.info("Creating a new Selenium WebDriver instance")
    return webdriver.Chrome(options=options, service=service)


def load_page_resources(driver):
    scroll = 1000

    logger.info("Waiting to load...")
    time.sleep(2)
    scroll_to(scroll, driver)
    time.sleep(2)
