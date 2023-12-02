import re

import typer
from src import craigslist as cl
from src import database as db
from src import facebook as fb
from src import utils

app = typer.Typer()

craigslistScraperVersion = 1
facebookScraperVersion = 1


@app.command()
def craigslist(event, context):
    utils.scrape("craigslist", craigslistScraperVersion)


@app.command()
def facebook(event, context):
    utils.scrape("facebook", facebookScraperVersion)


@app.command()
def link(link: str):
    clPattern = re.compile(
        r"^https://[a-zA-Z-]+\.craigslist\.org(?:/[^\s?]*)?(?:\?[^\s]*)?$"
    )
    fbPattern = re.compile(
        r"^https://www\.facebook\.com/marketplace(?:/[^\s?]*)?(?:\?[^\s]*)?$"
    )

    if clPattern.match(link):
        newInfo = cl.scrapeListing(link)
        db.update(link, newInfo)
    elif fbPattern.match(link):
        newInfo = fb.scrapeListing(link)
        print(newInfo)
    else:
        print("Not a Craigslist nor a Facebook Marketplace link")


if __name__ == "__main__":
    app()
