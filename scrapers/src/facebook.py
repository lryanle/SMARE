from bs4 import BeautifulSoup
import time
from . import utils

postClass = "x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24"
linkClass = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv"
thumbnailClass = "xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3"
titleClass = "x1lliihq x6ikm8r x10wlt62 x1n2onr6"
priceClass = "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u"
metaClass = "x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft"

listingInfoClass = "x78zum5 xdt5ytf x1iyjqo2 x1n2onr6"
listingSectionClass = "xod5an3"
bodyClass = "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"

def loadPageResources(driver):
	scroll = 100

	print("Waiting to load...")
	time.sleep(2)
	utils.scrollTo(scroll, driver)
	time.sleep(1.5)

	# Emulate a user scrolling
	for i in range(10):
		scroll += 1000
		utils.scrollTo(scroll, driver)
		time.sleep(1)


def setupURLs(oldestAllowedCars):
	# List of TX cities to scrape; can be expanded
	cities = ['houston', 'dallas', 'austin', 'fortworth', 'elpaso', 'sanantonio']

	# Set the URL of the Facebook Marketplace automotive category
	base_url = 'https://www.facebook.com/marketplace/{}/vehicles?minYear={}&exact=false'
	return [base_url.format(city, oldestAllowedCars) for city in cities]

def getAllPosts(browser):
	# Create a BeautifulSoup object from the HTML of the page
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	# Find all of the car listings on the page
	return soup.find_all('div', class_=postClass)

def getCarInfo(post):
	title = post.find('span', class_=titleClass).text

	print(f'Scraping "{title}"')

	price = post.find('span', class_=priceClass).text
	metadata = post.findAll('span', class_=metaClass)

	location = metadata[0].text
	odometer = metadata[1].text

	link = post.find('a', class_=linkClass, href=True)["href"]
	link = "https://facebook.com" + link
	
	thumbnail = post.find('img', class_=thumbnailClass)["src"]

	return title, price, location, odometer, link, [thumbnail]

def getCarImages():
	# class="x1a0syf3 x1ja2u2z"
	return "TODO"

def processAttributes(attributes):
	processedAttributes = []
	
	for attr in attributes:
		[label, value] = attr.split(": ")
		processedAttributes.append({"label": label, "value": value})

	return processedAttributes

def scrapeListing(url):
	browser = utils.setupBrowser()

	# Navigate to the URL
	print(f"Going to {url[0:60]}")
	browser.get(url[0:60]) 

	print(f"Loading page for {url[0:60]}")
	time.sleep(1)

	# Create a BeautifulSoup object from the HTML of the page
	html = browser.page_source
	soup = BeautifulSoup(html, 'html.parser')

	try:
		seeMoreButton = browser.find_element("class name", "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x6prxxf xvq8zen x1s688f xzsf02u".replace(" ", "."))
		utils.clickOn(seeMoreButton, browser)

		listingInfo = soup.find('div', class_=listingInfoClass)
		# description = listingInfo.find('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u")
		print(listingInfo)

		return 2

		# attributes = processAttributes([attr.text for attr in soup.findAll('p', class_="attrgroup")[1].findAll('span')])
		
		# map = soup.find('div', id='map')
		# longitude = map["data-longitude"]
		# latitude = map["data-latitude"]

		# print([attributes, description, longitude, latitude])
	except Exception as error:
		print(error)
		return -1	
	
	# Close the Selenium WebDriver instance
	browser.quit()
