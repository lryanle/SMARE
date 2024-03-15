# import necessary libraries
import datetime
import re

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
# drop unnecessary variables
# Look at the number of NA values by column
na_counts = cars.isna().sum()
# Drop columns with NA values greater than 15
cols_to_drop = na_counts[na_counts > 15].index
cars = cars.drop(columns=cols_to_drop)

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
# Drop rows with NaN values in the 'odometer' column
cars = cars.dropna(subset=['odometer'])
# Convert 'odometer' column to integers
cars['odometer'] = cars['odometer'].astype('int')
# create an age variable to get a better understanding of how old a car is
cars["age"] = datetime.date.today().year - cars["year"]

# Clean up the 'price' column by replacing non-numeric values with NaN
cars["price"] = pd.to_numeric(
    cars["price"].replace("[$,]", "", regex=True), errors="coerce"
)

# Fill NaN values in the 'price' column with a placeholder (you can choose a value that makes sense)
cars["price"].fillna(-1, inplace=True)

# Convert 'price' column to integers
cars["price"] = cars["price"].astype(int)
cars = cars[cars.price <= 100000]
