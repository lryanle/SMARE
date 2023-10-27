import time
from bs4 import BeautifulSoup
from homepage import setupBrowser

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
		
		print([attributes, description])
	except:
		print(f"Failed scraping {url}")		
	
	# Close the Selenium WebDriver instance
	browser.quit()

scrapeListing("https://abilene.craigslist.org/ctd/d/abilene-hyundai-elantra/7681061021.html")