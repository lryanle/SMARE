import re
import time
import pandas as pd

from bs4 import BeautifulSoup

from ..utilities import logger
from .utils import find_by_class, click_on, setup_browser

import csv
logger = logger.SmareLogger()

def make_link(line):
    words = line.split(" ")

    return f"https://www.kbb.com/{words[0]}/{'-'.join(words[1:-1])}/{words[-1]}"

def setup_url_df():
    file_path = '/var/task/src/scrapers/unique_missing_prices.csv'
    df = pd.read_csv(file_path, header=None, names=['car'])
    df = df.drop_duplicates()

    df.to_csv('unique_missing_prices.csv')

    df["link"] = df.apply(lambda row: make_link(row["car"]), axis=1)
    return df


def get_fair_price_avg(table):
    try:
        logger.debug("gonna look for the cells")

        price_cell_class = "css-irk93x ee33uo33"
        price_cells = table.find_all("td", class_=price_cell_class)

        logger.debug("gonna get the text out of em now")

        price_cells = [int(cell.text.strip().replace(",", "").replace("$", "")) for cell in price_cells[1::2]]

        logger.success(price_cells)
        return int(sum(price_cells) / len(price_cells))
    except Exception as e:
        logger.error(f"Error occurred while getting average price: {e}")
        return None


def scrape_car(url, car):
    time.sleep(4)
    try:
        browser = setup_browser()

        logger.info(f"Going to {url}")
        browser.get(url)
        logger.debug(f"Loading page for {url}")

        time.sleep(0.5)

        expand_button = find_by_class(browser, ".css-14tac3n.e1july540")
        if expand_button is not None:
            click_on(expand_button, browser)

        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", class_="css-1eade32 ee33uo30")
        avg = get_fair_price_avg(table)

        logger.debug(f"price: {avg}")
        browser.quit()

        with open('checkpoint.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow([car, avg])

        return avg
    except Exception as e:
        logger.error(f"Failed scraping {url}: {e}")

def run():
    df = setup_url_df()

    logger.info(f"scraping {len(df)} listings...")
    df["kbb_price"] = df.apply(lambda row: scrape_car(row["link"], row["car"]), axis=1)

    print(df.head())

    df.to_csv('kbb_scraper.csv', index=False)

    df.set_index('car', inplace=True)
    json_data = df['kbb_price'].to_json()
    with open('car_prices.json', 'w') as file:
        file.write(json_data)

    print(json_data)
