import typer
from src import utils
from src import craigslist as cl
from src import facebook as fb
from src import database as db

app = typer.Typer()

craigslistScraperVersion = 1
facebookScraperVersion = 1

@app.command()
def craigslist():
	utils.scrape("craigslist", craigslistScraperVersion)

@app.command()
def facebook():
	utils.scrape("facebook", facebookScraperVersion)

@app.command()
def link(link: str):
	if (".craigslist.org" in link):
		newInfo = cl.scrapeListing(link)
		db.update(link, newInfo)
	elif("https://www.facebook.com/marketplace" in link):
		newInfo = fb.scrapeListing(link)
		print(newInfo)
	else:
		print("Not a Craigslist nor a Facebook Marketplace link")

if __name__ == "__main__":
    app()