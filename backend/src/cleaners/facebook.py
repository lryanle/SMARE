import re

from ..utilities import logger
from .utils import extract_model as parse_model

logger = logger.SmareLogger()

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
    try:
        if attr == "odometer":
            return int(value.replace(",", ""))
        elif attr in ["highway_mpg", "city_mpg", "combined_mpg"]:
            return float(value)
        elif attr == "safety_rating":
            score, maxscore = value.split("/")
            return float(score) / float(maxscore)
        else:
            return value.lower()
    except ValueError as e:
        logger.error(f"Error cleaning attribute {attr} with value {value}: {e}")
        return None


def extract_attributes(attributes):
    output = {}
    try:
        # Extract attributes using regular expressions
        for attr_str in attributes:
            for attr, pattern in attrPatterns.items():
                match = re.search(pattern, attr_str)
                if match:
                    output[attr] = clean_attr(attr, match.group(1))
    except Exception as e:
        logger.error(f"Error extracting attributes: {e}")
    return output


def extract_model(title, make):
    try:
        return parse_model(title, make, r"^\d{4}\s+\w+\s+(([^\s\n]+\s+){0,4})")
    except Exception as e:
        logger.error(f"Error extracting model from title {title}: {e}")
    return None
