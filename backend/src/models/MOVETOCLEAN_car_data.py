import re
from difflib import get_close_matches
import json
import cleaner
cars = cleaner.cars

# Dictionary of car makes
kbb_make = ["acura", "alfa-romeo", "aston-martin", "audi", "bentley", "bmw", "buick", "cadillac", "chevrolet", "chrysler", "dodge", "ferrari", "fiat", "ford", "genesis", "gmc", "honda", "hyundai", "infiniti", "jaguar", "jeep", "kia", "lamborghini", "landrover", "lexus", "lincoln", "lucid", "maserati", "mazda", "mclaren", "mercedes-benz", "mini", "mitsubishi", "nissan", "polestar", "porsche", "ram", "rivian", "rolls-royce", "subaru", "tesla", "toyota", "volkswagen", "volvo"]

with open("kbb_data.json") as kbbjson:
    kbb_models = json.load(kbbjson) 

title = cars["title"]


# Function to extract make from title
def extract_make(title):
    title_lower = title.lower()
    for make in kbb_make:
        if make in title_lower:
            return make
        elif len(make) >= 4 and make[:4] in title_lower:
            return make
    return None


def extract_model_wreg(title, make):
    # Check if the make is in the kbb_models dictionary
    make_models = kbb_models.get(make, [])
    # Use regex to find patterns like "2021 RAM 3500" in the title
    match = re.search(r"\b\d{4}\s*[a-zA-Z0-9-]+\s*([a-zA-Z0-9-]+)\b", title)
    if match:
        # Extracted model is in the first capturing group
        model = match.group(1)
        if model is not None:
            # Handle models with dashes
            model = model.replace("-", "")
            # Compare with the kbb_models dictionary
            matched_model = get_close_matches(model, make_models, n=1)
            if matched_model:
                return matched_model[0]
            else:
                # If no direct match, try finding a close match using pieces of words
                title_words = re.findall(r"\b\w+\b", title)
                extracted_model_pieces = []
                for word in title_words:
                    # Check if the word is part of the make name, if yes, skip it
                    if make is not None and word.lower() in make.lower():
                        continue
                    extracted_model_pieces.append(word)
                    current_model_attempt = " ".join(extracted_model_pieces)
                    # Check if the current attempt is a close match
                    matched_model = get_close_matches(
                        current_model_attempt, make_models, n=1
                    )
                    if matched_model:
                        return matched_model[0]
                # If still no match, return the original extracted model
                return model
        else:
            return None
    else:
        return None


# Apply the extraction functions
cars["manufacturer"] = cars["title"].apply(extract_make)
cars["model"] = cars.apply(
    lambda row: extract_model_wreg(row["title"], row["manufacturer"]), axis=1
)

# Drop rows where either 'manufacturer' or 'model' is empty
cars.dropna(subset=["manufacturer", "model"], inplace=True)

numeric_columns = ["price", "year", "odometer", "age"]
