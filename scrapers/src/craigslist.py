import time
import re

from bs4 import BeautifulSoup


def setupURLs(oldestAllowedCars):
    # List of TX cities to scrape; can be expanded
    cities = [
        "abilene",
        "amarillo",
        "austin",
        "beaumont",
        "brownsville",
        "collegestation",
        "corpuschristi",
        "dallas",
        "nacogdoches",
        "delrio",
        "elpaso",
        "galveston",
        "houston",
        "killeen",
        "laredo",
        "lubbock",
        "mcallen",
        "odessa",
        "sanangelo",
        "sanantonio",
        "sanmarcos",
        "bigbend",
        "texoma",
        "easttexas",
        "victoriatx",
        "waco",
        "wichitafalls",
    ]

    # Set the URL of the Facebook Marketplace automotive category
    base_url = (
        "https://{}.craigslist.org/search/cta?min_auto_year={}&min_price=1#search=1~gallery~0~0"
    )
    return [base_url.format(city, oldestAllowedCars) for city in cities]


def getAllPosts(browser):
    # Create a BeautifulSoup object from the HTML of the page
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find all of the car listings on the page
    return soup.find_all("div", class_="gallery-card")


def getCarInfo(post):
    title = post.find("span", class_="label").text

    print(f'Scraping "{title}"')

    price = post.find("span", class_="priceinfo").text
    metadata = post.find("div", class_="meta").text.split("·")

    odometer = metadata[1]
    if len(metadata) >= 3:
        location = metadata[2]

    link = post.find("a", class_="posting-title", href=True)["href"]

    return {
        "title": title,
        "price": price,
        "location": location,
        "odometer": odometer,
        "link": link
    }


def processAttributes(attributes):
    processedAttributes = []

    for attr in attributes:
        label = attr.find("span", class_="labl").text.replace(":", "").replace(" ", "-").lower()
        value = attr.find("span", class_="valu").text

        processedAttributes.append({"label": label, "value": value})

    return processedAttributes


def scrapeListing(url, browser):
    # Navigate to the URL
    print(f"Going to {url}")
    browser.get(url)

    print(f"Loading page for {url}")
    time.sleep(1)

    # Create a BeautifulSoup object from the HTML of the page
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    try:
        description = soup.find("section", id="postingbody").text

        year = soup.find("span", class_="valu year").text
        makeModel = soup.find("a", class_="valu makemodel").text

        attributeGroups = soup.find_all("div", class_="attr")
        attributes = processAttributes(attributeGroups[1:])

        imgThumbnails = soup.find("div", id="thumbs")

        images = [
            img["src"]
            for img in imgThumbnails.find_all("img")
        ]

        map = soup.find("div", id="map")
        longitude = map["data-longitude"]
        latitude = map["data-latitude"]
    except Exception as e:
        print(f"Failed scraping {url}: \n{e}")
        return None

    # Close the Selenium WebDriver instance
    browser.quit()
    return {
        "postBody": description,
        "year": year,
        "makeModel": makeModel,
        "latitude": latitude,
        "longitude":longitude,
        "attributes": attributes,
        "images": images
    }