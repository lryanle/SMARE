# import necessary libraries
import datetime
import re
from difflib import get_close_matches
import pandas as pd

from .. import database as db

# Fetch data from MongoDB and convert it to a DataFrame
cursor = db.findAllCars()
data = list(cursor)
cars = pd.DataFrame(data)

# Convert DataFrame to CSV
csv_filename = "output_data.csv"
cars.to_csv(csv_filename, index=False)

print(f"Data has been successfully exported to {csv_filename}")

cars = pd.read_csv("output_data.csv")

# DATA CLEANING
# drop unnecessary variables: id, url
cars = cars.drop(
    columns=[
        "source",
        "link",
        "location",
        "scraper-version",
        "scrape-date",
        "images",
        "postBody",
        "latitude",
        "longitude",
        "year",
        "attributes",
        "makeModel",
    ]
)

# drop NA values
cars = cars.dropna()

cars["odometer"] = cars["odometer"].apply(
    lambda x: (
        int(re.search(r"\d+", str(x)).group(0)) if re.search(r"\d+", str(x)) else None
    )
)
cars["year"] = cars["title"].str.extract(r"(\d{4})")
# Fill NaN values in the 'year' column with a placeholder
cars["year"].fillna(-1, inplace=True)
cars = cars.astype({"year": "int", "odometer": "int"})

# create an age variable to get a better understanding of how old a car is
cars["age"] = datetime.date.today().year - cars["year"]

cars = cars[cars.year >= 2005]

ars = cars[cars.odometer <= 300]
# Clean up the 'price' column by replacing non-numeric values with NaN
cars["price"] = pd.to_numeric(
    cars["price"].replace("[$,]", "", regex=True), errors="coerce"
)

# Fill NaN values in the 'price' column with a placeholder (you can choose a value that makes sense)
cars["price"].fillna(-1, inplace=True)

# Convert 'price' column to integers
cars["price"] = cars["price"].astype(int)
cars = cars[cars.price <= 100000]
