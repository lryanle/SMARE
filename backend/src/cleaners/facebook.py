import re
import json

from difflib import get_close_matches

# Define patterns for different attributes
attrPatterns = {
    "odometer": r"Driven\s*([\d,]+)\s*miles",
    "transmission": r"^([A-Za-z]+)\s*transmission",
    "safety_rating": r"(\d/\d)\s*overall\s*NHTSA\s*safety\s*rating",
    "fuel_type": r"Fuel\s*type:\s*([A-Za-z]+)",
    "city_mpg": r"(\d+\.\d+)\s*MPG\s*city",
    "highway_mpg": r"(\d+\.\d+)\s*MPG\s*highway",
    "combined_mpg": r"(\d+\.\d+)\s*MPG\s*combined",
    "exterior_color": r"Exterior\s*color:\s*([A-Za-z]+\s[A-Za-z]+?)\s",
    "interior_color": r"Interior\s*color:\s*([A-Za-z]+\s[A-Za-z]+?)$",
    "title": r"([A-Za-z]+)\s*title",
    "condition": r"([A-Za-z]+\s[A-Za-z]+?)\s*condition",
}


def clean_attr(attr, value):
    if attr == "odometer":
        return int(value.replace(",", ""))
    elif attr == "highway_mpg" or attr == "city_mpg" or attr == "combined_mpg":
        return float(value)
    elif attr == "safety_rating":
        score, maxscore = value.split("/")
        return float(score) / float(maxscore)
    else:
        return value.lower()


def extract_attributes(attributes):
    output = {}

    # Extract attributes using regular expressions
    for attr_str in attributes:
        for attr, pattern in attrPatterns.items():
            match = re.search(pattern, attr_str)
            if match:
                output[attr] = clean_attr(attr, match.group(1))

    return output


def extract_year(title_str):
    year = re.match(r"^20\d{2}", title_str)

    if not year:
        return None

    return int(year.group(0))

def extract_model_wreg(title, make):
    with open("kbb_data.json") as kbbjson:
        models = json.load(kbbjson)

    # Use regex to find patterns like "2021 RAM 3500" in the title
    match = re.search(r"\b\d{4}\s*[a-zA-Z0-9-]+\s*([a-zA-Z0-9-]+)\b", title)
    
    if not match:
        return None
    
    model = match.group(1)
    
    if model is not None:
        # Handle models with dashes
        model = model.replace("-", "")
        # Compare with the kbb_models dictionary
        matched_model = get_close_matches(model, models[make], n=1)
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
                    current_model_attempt, models[make], n=1
                )
                if matched_model:
                    return matched_model[0]
            # If still no match, return the original extracted model
            return model
    else:
        return None
