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


def cleanAttr(attr, value):
    if attr == 'odometer':
        return int(value.replace(",", ""))
    elif attr == 'highwayMpg' or attr == 'cityMpg' or attr == 'combinedMpg':
        return float(value)
    elif attr == 'safetyRating':
        score, max = value.split('/')
        return float(score) / float(max)
    else:
        return value.lower()


def extractAttributes(attributes):
    output = {}

    # Extract attributes using regular expressions
    for attrStr in attributes:
        for attr, pattern in attrPatterns.items():
            match = re.search(pattern, attrStr)
            if match:
                output[attr] = cleanAttr(attr, match.group(1))

    return output