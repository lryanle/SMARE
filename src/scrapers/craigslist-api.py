from datetime import datetime
import csv
import json
import requests

location_to_batch = {
	"newyork": "3-0-360-0-0",
	"philadelphia": "17-0-360-0-0",
	"dallas": "21-0-360-0-0",
	# Add more locations and their batch values as needed
}

def clean_price_str(str):
	price_str = str.replace("$", "").replace(",", "")
	return float(price_str)

def fetch_job_postings(location, category):
	base_url = "https://sapi.craigslist.org/web/v8/postings/search/full"

	# Get the batch value and category abbreviation from the mappings
	# Default to New York if location not found
	batch = location_to_batch.get(location)

	params = {
		'batch': batch,
		'cc': 'US',
		'lang': 'en',
		'searchPath': "cta",
		"id": "0",
  		"collectContactInfo": True,
	}

	headers = {
		'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
		'Referer': f'https://{location}.craigslist.org/',
		'sec-ch-ua-mobile': '?0',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
		'sec-ch-ua-platform': '"Windows"',
		'Cookie': f'cl_b=COOKIE VALUE'
	}

	response = requests.get(base_url, params=params, headers=headers)

	if response.status_code == 200:
		data = response.json()

		with open('file.txt', 'w') as f:
			json.dump(data["data"]["items"], f, indent=2)
	else:
		print("Failed to retrieve data. Status code:", response.status_code)
		data = None


	car_posts = []
	if data:
		# For each car post found
		for post in data["data"]["items"]:
			title = None
			price = None
			mileage = None
			partial_link = None

			for element in post:
				if isinstance(element, str):
					title = element
				elif isinstance(element, list) and len(element) > 0 and element[0] == 10:
					price = clean_price_str(element[1])
				elif isinstance(element, list) and len(element) > 0 and element[0] == 9:
					mileage = element[1]
				elif isinstance(element, list) and len(element) > 0 and element[0] == 6:
					partial_link = element[1]
			if title and price and mileage and partial_link:
				car_posts.append((title, price, mileage, partial_link))
		return car_posts
	else:
		print("No data available.")

if __name__ == "__main__":
	location = "dallas"
	category = "cta"
	
	car_posts = fetch_job_postings(location, category)

	if car_posts:
		current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
		category = category.replace("/", "&")
		csv_filename = f"{location}_{category}_openings_{current_datetime}.csv"

		with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
			writer = csv.writer(file)

			writer.writerow(["Title", "Price", "Mileage", "Partial HTML Path"])
			for car in car_posts:
				writer.writerow([car[0], car[1], car[2], car[3]])
	
		print(f"Car posts have been saved to {csv_filename}")
	else:
		print("No car posts were found. Nothing was saved")