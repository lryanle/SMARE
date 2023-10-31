import craigslist as cl
import database as db
from typing import Optional
import typer
from typing_extensions import Annotated

app = typer.Typer()

@app.command()
def craigslist(minYear: Annotated[Optional[int], typer.Argument()] = 2011):
	cityURLs = cl.setupURLs(minYear)
	browser = cl.setupBrowser()

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