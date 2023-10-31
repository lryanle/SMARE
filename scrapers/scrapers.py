import typer
import craigslist
import facebook
import utils

app = typer.Typer()

@app.command()
def craigslist():
	utils.scrape(craigslist, "craigslist")

@app.command()
def facebook():
	utils.scrape(facebook, "facebook")

@app.command()
def link(link: str):
	if (".craigslist.org" in link):
		craigslist.scrapeListing(link)
	elif("https://www.facebook.com/marketplace" in link):
		facebook.scrapeListing(link)
	else:
		print("Not a Craigslist nor a Facebook Marketplace link")

if __name__ == "__main__":
    app()