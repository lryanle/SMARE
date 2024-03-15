from .utils import clean_odometer

def extract_attributes(attributes):
    output = {}

    # Extract attributes using regular expressions
    for attr_obj in attributes:
        output[attr_obj["label"]] = attr_obj["value"]

    output["odometer"] = clean_odometer(output["odometer"])

    return output

def str_to_num(car):
    clean_car = {}

    clean_car["year"] = int(car["year"])
    clean_car["latitude"] = float(car["latitude"])
    clean_car["longitude"] = float(car["longitude"])

    return clean_car
