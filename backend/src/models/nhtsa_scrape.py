import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_nhtsa_data(url):
    data = []
    page_num = 0
    driver = webdriver.Chrome()  # Change this to your preferred WebDriver
    
    try:
        driver.get(url)
        
        # Click the "Apply" button
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "edit-submit-vehicle-theft-data"))
        )
        apply_button.click()
        
        while page_num < 130:  # Limit to first 100 pages
            time.sleep(2)  # Wait for the table to load
            
            # Parse the HTML content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'class': 'cols-8 table d8-port views-table'})
            if not table:
                print(f"No table found on page {page_num}. Exiting.")
                break
            
            # Extract data from the table
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cols = row.find_all('td')
                if len(cols) >= 8:  # Ensure all columns are present
                    year = cols[0].text.strip()
                    manufacturer = cols[1].text.strip()
                    make = cols[2].text.strip()
                    make_model = cols[3].text.strip()
                    thefts = cols[4].text.strip()
                    production = cols[5].text.strip()
                    rate = cols[6].text.strip()
                    theft_type = cols[7].text.strip()
                    
                    data.append({
                        "year": year,
                        "manufacturer": manufacturer,
                        "make": make,
                        "make_model": make_model,
                        "thefts": thefts,
                        "production": production,
                        "rate": rate,
                        "type": theft_type
                    })
            
            # Check if there is a next page button
            next_page_button = driver.find_element(By.CSS_SELECTOR, "li.pager-next a")
            if next_page_button:
                next_page_button.click()
                page_num += 1
            else:
                print("No more pages found. Exiting.")
                break
                
    finally:
        driver.quit()
        
    return data


def main():
    url = "https://www.nhtsa.gov/road-safety/vehicle-theft-prevention/theft-rates"
    data = scrape_nhtsa_data(url)
    
    # Save data to JSON file
    with open('nhtsa_theft_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Data saved to 'nhtsa_theft_data.json'.")

if __name__ == "__main__":
    main()
