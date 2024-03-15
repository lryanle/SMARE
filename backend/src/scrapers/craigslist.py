import time

from bs4 import BeautifulSoup


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
    # Create a BeautifulSoup object from the HTML of the page
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Find all of the car listings on the page
    return soup.find_all("div", class_="gallery-card")


def get_car_info(post):
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
        "link": link,
    }


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
        make_model = soup.find("a", class_="valu makemodel").text

        attribute_groups = soup.find_all("div", class_="attr")
        attributes = process_attributes(attribute_groups[1:])

        img_thumbnails = soup.find("div", id="thumbs")

        images = [img["src"] for img in img_thumbnails.find_all("img")]

        physical_map = soup.find("div", id="map")
        longitude = physical_map["data-longitude"]
        latitude = physical_map["data-latitude"]
    except Exception as e:
        print(f"Failed scraping {url}: \n{e}")
        return None

    return {
        "post_body": description,
        "year": year,
        "makemodel": make_model,
        "latitude": latitude,
        "longitude": longitude,
        "attributes": attributes,
        "images": images,
    }
