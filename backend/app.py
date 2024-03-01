import typer
from src.scrapers import utils as scrapeUtil

app = typer.Typer()

craigslistScraperVersion = 4
facebookScraperVersion = 4

duplicateTerminationLimit = 5


@app.command()
def craigslist(event, context):
    scrapeUtil.scrape("craigslist", craigslistScraperVersion, duplicateTerminationLimit)


@app.command()
def facebook(event, context):
    scrapeUtil.scrape("facebook", facebookScraperVersion, duplicateTerminationLimit)


if __name__ == "__main__":
    app()
