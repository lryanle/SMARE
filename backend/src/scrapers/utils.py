import time

from selenium import webdriver


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
