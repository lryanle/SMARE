import typer
from src import utils

app = typer.Typer()

craigslistScraperVersion = 4
facebookScraperVersion = 4

duplicateTerminationLimit = 5


@app.command()
def craigslist(event, context):
    utils.scrape("craigslist", craigslistScraperVersion, duplicateTerminationLimit)


@app.command()
def facebook(event, context):
    utils.scrape("facebook", facebookScraperVersion, duplicateTerminationLimit)


if __name__ == "__main__":
    app()
