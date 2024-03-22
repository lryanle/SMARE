import time

from bs4 import BeautifulSoup

from ..utilities import logger
from . import utils

logger = logger.SmareLogger()

postClass = (
    "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4"
    " x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24"
)
linkClass = (
    "x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l "
    "x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm "
    "xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg "
    "xggy1nq x1a2a7pz x1heor9g x1lku1pv"
)

thumbnailClass = "xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3"
titleClass = "x1lliihq x6ikm8r x10wlt62 x1n2onr6"
priceClass = "x78zum5 x1q0g3np x1iorvi4 x4uap5 xjkvuk6 xkhd6sd"

metaClass = "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"

listingInfoClass = "x78zum5 xdt5ytf x1iyjqo2 x1n2onr6"
listingSectionClass = "xod5an3"
bodyClass = (
    "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx"
    " x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty"
    " x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"
)


def setup_urls(oldest_allowed_cars):
    # List of TX cities to scrape; can be expanded
    cities = ["houston", "dallas", "austin", "fortworth", "elpaso", "sanantonio"]

    # Set the URL of the Facebook Marketplace automotive category
    base_url = "https://www.facebook.com/marketplace/{}/vehicles?minYear={}&exact=false"
    return [base_url.format(city, oldest_allowed_cars) for city in cities]


def get_all_posts(browser):
    try:
        # Create a BeautifulSoup object from the HTML of the page
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        return soup.find_all("div", class_=postClass)
    except Exception as e:
        logger.error(f"Failed to get page source: {e}")
        return []


def get_car_info(post):
    try:
        title = post.find("span", class_=titleClass).text
        logger.debug(f'Scraping "{title}"')

        price = post.find("div", class_=priceClass).text
        metadata = post.findAll("span", class_=metaClass)

        location = metadata[0].text
        odometer = metadata[1].text

        link = post.find("a", class_=linkClass, href=True)["href"]
        link = "https://facebook.com" + link

        return {
            "title": title,
            "price": price,
            "location": location,
            "odometer": odometer,
            "link": link,
        }
    except AttributeError as e:
        logger.error(f"Failed to extract car info: {e}")
        return {}


def scrape_listing(url, browser):
    try:
        # Navigate to the URL
        logger.debug(f"Going to {url}")
        browser.get(url)

        logger.debug(f"Loading page for {url}")
        time.sleep(1)

        # Find div with the current listing's info
        listing = browser.find_elements(
            "class name",
            "x1jx94hy x78zum5 xdt5ytf x1lytzrv x6ikm8r x10wlt62 xiylbte xtxwg39".replace(
                " ", "."
            ),
        )[0]
        see_more_button = listing.find_elements(
            "class name",
            "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x6prxxf xvq8zen x1s688f xzsf02u".replace(
                " ", "."
            ),
        )[0]

        utils.click_on(see_more_button, browser)

        # Create a BeautifulSoup object from the HTML of the page
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        try:
            listing = soup.find(
                "div",
                class_="x1jx94hy x78zum5 xdt5ytf x1lytzrv x6ikm8r x10wlt62 xiylbte xtxwg39",
            )

            images_html = listing.find_all("img")
            images = []

            for img in images_html:
                images.append(img["src"].replace("amp;", ""))

            description_html = listing.find(
                "div", class_="xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a"
            )
            description = description_html.find(
                "span",
                class_=(
                    "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv "
                    "xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc "
                    "x6prxxf xvq8zen xo1l8bm xzsf02u"
                ),
            ).text

            # About this car: class="x1gslohp"
            about_vehicle = listing.find("div", class_="x1gslohp")
            atrributes_html = about_vehicle.find_all(
                "span",
                class_=(
                    "x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv "
                    "xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x41vudc "
                    "x6prxxf xvq8zen xo1l8bm xzsf02u"
                ),
            )
            attributes = []

            for attr in atrributes_html:
                attributes.append(attr.text)

            # Typical features: x1gslohp x11i5rnm x12nagc x1mh8g0r
        except Exception as err:
            logger.error(f"Failed scraping {url}: \n{err}")
            return None
    except Exception as e:
        logger.error(f"Failed to scrape listing: {e}")
        return {}

    return {"post_body": description, "attributes": attributes, "images": images}
