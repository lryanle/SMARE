import re
import time

from bs4 import BeautifulSoup

from ..utilities import logger

logger = logger.SmareLogger()


def setup_urls(oldest_allowed_cars):
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
    base_url = "https://{}.craigslist.org/search/cta?min_auto_year={}&min_price=1#search=1~gallery~0~0"
    return [base_url.format(city, oldest_allowed_cars) for city in cities]


def get_all_posts(browser):
    try:
        # Create a BeautifulSoup object from the HTML of the page
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find all of the car listings on the page
        return soup.find_all("div", class_="gallery-card")
    except Exception as e:
        logger.error(f"Error occurred while getting posts: {e}")
        return []


def is_website(str):
    match = re.match(
        r"www[\.\-_\s]|[a-zA-Z0-9-]+[\.\s\-_][a-zA-Z]{2,}|[a-zA-Z0-9-]+[\.\s\-_][a-zA-Z]{2,}[\.\s\-_][a-zA-Z]{2,}",
        str,
    )

    return bool(match)


def get_car_info(post):
    try:
        title = post.find("span", class_="label").text
        logger.debug(f'Scraping "{title}"')

        price = post.find("span", class_="priceinfo").text
        metadata = post.find("div", class_="meta").text.split("·")

        odometer = metadata[1].strip()
        location = metadata[2].strip() if len(metadata) >= 3 else "Unknown location"

        link = post.find("a", class_="posting-title", href=True)["href"]

        car_info = {
            "title": title,
            "price": price,
            "odometer": odometer,
            "link": link,
        }

        if is_website(location):
            car_info["seller_website"] = location
        else:
            car_info["location"] = location

        return car_info
    except Exception as e:
        logger.error(f"Error occurred while getting car info: {e}")
        return {}


def process_attributes(attributes):
    processed_attributes = []

    for attr in attributes:
        label = (
            attr.find("span", class_="labl")
            .text.replace(":", "")
            .replace(" ", "_")
            .lower()
        )
        value = attr.find("span", class_="valu").text

        processed_attributes.append({"label": label, "value": value})

    return processed_attributes


def scrape_listing(url, browser):
    try:
        logger.info(f"Going to {url}")
        browser.get(url)
        logger.debug(f"Loading page for {url}")
        time.sleep(1)

        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        description = soup.find("section", id="postingbody").text.strip()
        year = soup.find("span", class_="valu year").text.strip()
        make_model = soup.find("span", class_="valu makemodel").text.strip()

        attribute_groups = soup.find_all("div", class_="attr")
        attributes = process_attributes(attribute_groups[1:])

        img_thumbnails = soup.find("div", id="thumbs")
        images = [img["src"] for img in img_thumbnails.find_all("img")]

        physical_map = soup.find("div", id="map")
        longitude = physical_map["data-longitude"]
        latitude = physical_map["data-latitude"]

        return {
            "post_body": description,
            "year": year,
            "makemodel": make_model,
            "latitude": latitude,
            "longitude": longitude,
            "attributes": attributes,
            "images": images,
        }
    except Exception as e:
        logger.error(f"Failed scraping {url}: {e}")
        return {}
