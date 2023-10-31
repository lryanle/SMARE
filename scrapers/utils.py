from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import utils
import database as db

def scrollTo(x, driver):
	driver.execute_script(f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})")

def setupBrowser():
	print("Setting up headless browser")

	options = Options()
	options.add_argument("--headless=new")

	print("Creating a new Selenium WebDriver instance")
	return webdriver.Chrome(options=options)

def scrape(scraper, website):
	cityURLs = scraper.setupURLs(2011)
	browser = utils.setupBrowser()

	for url in cityURLs:
		print(f"Going to {url}")
		browser.get(url) 

		print(f"Loading cars from {url}")
		scraper.loadPageResources(browser)

		carPosts = scraper.getAllPosts(browser)

		for post in carPosts:
			try:
				title, price, location, odometer, link, images = scraper.getCarInfo(post)
				db.post_raw(website, title, price, location, odometer, link, images)
			except Exception as error:
				print(error)
				
	browser.quit()