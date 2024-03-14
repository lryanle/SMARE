import re


# Define patterns for different attributes
attrPatterns = {
    'odometer': r'Driven\s*([\d,]+)\s*miles',
    'transmission': r'^([A-Za-z]+)\s*transmission',
    'safetyRating': r'(\d/\d)\s*overall\s*NHTSA\s*safety\s*rating',
    'fuelType': r'Fuel\s*type:\s*([A-Za-z]+)',
    'cityMpg': r'(\d+\.\d+)\s*MPG\s*city',
    'highwayMpg': r'(\d+\.\d+)\s*MPG\s*highway',
    'combinedMpg': r'(\d+\.\d+)\s*MPG\s*combined',
    'exteriorColor': r'Exterior\s*color:\s*([A-Za-z]+\s[A-Za-z]+?)\s',
    'interiorColor': r'Interior\s*color:\s*([A-Za-z]+\s[A-Za-z]+?)$',
    'title': r'([A-Za-z]+)\s*title',
    'condition': r'([A-Za-z]+\s[A-Za-z]+?)\s*condition',
}


def clean_attr(attr, value):
    if attr == 'odometer':
        return int(value.replace(",", ""))
    elif attr == 'highwayMpg' or attr == 'cityMpg' or attr == 'combinedMpg':
        return float(value)
    elif attr == 'safetyRating':
        score, maxscore = value.split('/')
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
