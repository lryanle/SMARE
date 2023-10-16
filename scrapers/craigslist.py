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
	else:
		print("Failed to retrieve data. Status code:", response.status_code)
		data = None

	job_postings = []
	with open('file.txt', 'w') as f:
		json.dump(data, f, indent=2)

	if data:
		for item in data["data"]["items"]:
			job_title = None
			commission = None
			for element in item:
				if isinstance(element, str):
					job_title = element
				elif isinstance(element, list) and len(element) > 0 and element[0] == 7:
					commission = element[1]
			if job_title and commission:
				job_postings.append((job_title, commission))
		return job_postings
							
	else:
		print("No data available.")

if __name__ == "__main__":
	location = "dallas"
	category = "cta"
	
	job_postings = fetch_job_postings(location, category)

	if job_postings:
		current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
		category = category.replace("/", "&")
		csv_filename = f"{location}_{category}_openings_{current_datetime}.csv"

		with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
			writer = csv.writer(file)

			writer.writerow(["Job Title", "Commission"])
			for job in job_postings:
				writer.writerow([job[0], job[1]])
	
		print(f"Job postings have been saved to {csv_filename}")
	else:
		print("No data available.")