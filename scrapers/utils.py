from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrollTo(x, driver):
	driver.execute_script(f"window.scrollTo({{top: {x}, left: 100, behavior: 'smooth'}})")

def setupBrowser():
	print("Setting up headless browser")

	options = Options()
	options.add_argument("--headless=new")

	print("Creating a new Selenium WebDriver instance")
	return webdriver.Chrome(options=options)