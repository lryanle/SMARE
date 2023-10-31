from typing import Optional
from typing_extensions import Annotated
import typer

import craigslist as cl
import facebook as fb
import database as db
import utils

app = typer.Typer()

@app.command()
def craigslist(minYear: Annotated[Optional[int], typer.Argument()] = 2011):
	cityURLs = cl.setupURLs(minYear)
	browser = utils.setupBrowser()

	for url in cityURLs:
		print(f"Going to {url}")
		browser.get(url) 

		print(f"Loading cars from {url}")
		cl.loadPageResources(browser)

		carPosts = cl.getAllPosts(browser)

		for post in carPosts:
			try:
				title, price, location, odometer, link, images = cl.getCarInfo(post)
				db.post_raw("craigslist", title, price, location, odometer, link, images)
			except Exception as error:
				print(error)
				
	browser.quit()

@app.command()
def link(link: str):
	if (".craigslist.org" in link):
		cl.scrapeListing(link)
	elif("https://www.facebook.com/marketplace" in link):
		print("facebook marketplace")
	else:
		print("Not a Craigslist nor a Facebook Marketplace link")

if __name__ == "__main__":
    app()