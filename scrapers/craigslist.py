from bs4 import BeautifulSoup
import time
import utils

def loadPageResources(driver):
	scroll = 100

	print("Waiting to load...")
	time.sleep(2)

	utils.scrollTo(scroll, driver)

	loadImgButtons = driver.find_elements("class name", "slider-back-arrow")

	time.sleep(2)

	# Emulate a user scrolling
	for i in range(len(loadImgButtons)):
		scroll += 100
		utils.scrollTo(scroll, driver)

		driver.execute_script("arguments[0].click();", loadImgButtons[i])

		time.sleep(.5)


def setupURLs(oldestAllowedCars):
	# List of TX cities to scrape; can be expanded
	cities = ["abilene", "amarillo", "austin", "beaumont", "brownsville", "collegestation", "corpuschristi", "dallas", "nacogdoches", "delrio", "elpaso", "galveston", "houston", "killeen", "laredo", "lubbock", "mcallen", "odessa", "sanangelo", "sanantonio", "sanmarcos", "bigbend", "texoma", "easttexas", "victoriatx", "waco", "wichitafalls"]

	# Set the URL of the Facebook Marketplace automotive category
	base_url = 'https://{}.craigslist.org/search/cta?min_auto_year={}#search=1~gallery~0~0'
	return [base_url.format(city, oldestAllowedCars) for city in cities]

def getAllPosts(browser):
	# Create a BeautifulSoup object from the HTML of the page
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	# Find all of the car listings on the page
	return soup.find_all('div', class_='gallery-card')

def getCarInfo(post):
	title = post.find('span', class_='label').text

	print(f'Scraping "{title}"')

	price = post.find('span', class_='priceinfo').text
	metadata = post.find('div', class_="meta").text.split('·')

	odometer = metadata[1]
	if (len(metadata) >= 3):
		location = metadata[2]
	
	link = post.find('a', class_='posting-title', href=True)["href"]
	
	imageElements = post.findAll('img')
	images = [img["src"] for img in imageElements]

	return title, price, location, odometer, link, images

def processAttributes(attributes):
	processedAttributes = []
	
	for attr in attributes:
		[label, value] = attr.split(": ")
		processedAttributes.append({"label": label, "value": value})

	return processedAttributes

def scrapeListing(url):
	browser = setupBrowser()

	# Navigate to the URL
	print(f"Going to {url}")
	browser.get(url) 

	print(f"Loading page for {url}")
	time.sleep(1)

	# Create a BeautifulSoup object from the HTML of the page
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	try:
		description = soup.find('section', id='postingbody').text
		attributes = processAttributes([attr.text for attr in soup.findAll('p', class_="attrgroup")[1].findAll('span')])
		
		map = soup.find('div', id='map')
		longitude = map["data-longitude"]
		latitude = map["data-latitude"]

		print([attributes, description, longitude, latitude])
	except:
		print(f"Failed scraping {url}")		
	
	# Close the Selenium WebDriver instance
	browser.quit()