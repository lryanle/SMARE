from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import date

def scrollTo(x, driver):
    driver.execute_script(f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})")

def loadPageResources(driver):
    scroll = 100

    print("Waiting to load...")
    time.sleep(2)

    scrollTo(scroll, driver)

    loadImgButtons = driver.find_elements("class name", "slider-back-arrow")

    time.sleep(2)

    # Emulate a user scrolling
    for i in range(len(loadImgButtons)):
        scroll += 100
        scrollTo(scroll, driver)

        driver.execute_script("arguments[0].click();", loadImgButtons[i])

        time.sleep(.5)


def setupURLs():
    #list of cities to scrape; can be expanded
    cities = ["abilene", "amarillo", "austin", "beaumont", "brownsville", "collegestation", "corpuschristi", "dallas", "nacogdoches", "delrio", "elpaso", "galveston", "houston", "killeen", "laredo", "lubbock", "mcallen", "odessa", "sanangelo", "sanantonio", "sanmarcos", "bigbend", "texoma", "easttexas", "victoriatx", "waco", "wichitafalls"]

    oldestAllowedCars = 2011

    # Set the URL of the Facebook Marketplace automotive category
    base_url = 'https://{}.craigslist.org/search/cta?min_auto_year={}#search=1~gallery~0~0'
    return [base_url.format(city, oldestAllowedCars) for city in cities]

def setupBrowser():
    print("Setting up headless browser")

    options = Options()
    # options.add_argument("--headless=new")

    print("Creating a new Selenium WebDriver instance")
    return webdriver.Chrome(options=options)

def getAllPosts(browser):
    # Create a BeautifulSoup object from the HTML of the page
    html = browser.page_source
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Find all of the car listings on the page
    return soup.find_all('div', class_='gallery-card')

def getCarImages():
    return "TODO"

def scrapeCarInfo(post):
    title = post.find('span', class_='label').text

    print(f'Scraping "{title}"')

    price = post.find('span', class_='priceinfo').text
    metadata = post.find('div', class_="meta").text.split('·')

    miles = metadata[1]
    if (len(metadata) >= 3):
        location = metadata[2]
    
    link = post.find('a', class_='posting-title', href=True)["href"]
    
    imageElements = post.findAll('img')
    images = [img["src"] for img in imageElements]

    return {
        "title": title, 
        "price": price, 
        "location": location, 
        "miles": miles, 
        "link": link,
        "images": images,
        "scrapeDate": date.today()
    }

def scrapeCraigslist():
    cityURLs = setupURLs()
    browser = setupBrowser()

    # Create a list to store the scraped data
    print("Started scraping...")

    for url in cityURLs:
        # Navigate to the URL
        print(f"Going to {url}")
        browser.get(url) 

        print(f"Loading cars from {url}")

        loadPageResources(browser)

        carPosts = getAllPosts(browser)

        # Iterate over the listings and scrape the data
        for post in carPosts:
            try:
                car = scrapeCarInfo(post)
                print(car)
            except:
                print("Incomplete listing info")
                
    # Close the Selenium WebDriver instance
    browser.quit()

if (__name__ == "__main__"):
    scrapeCraigslist()