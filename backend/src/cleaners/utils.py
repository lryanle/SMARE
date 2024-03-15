from difflib import SequenceMatcher

def clean_currency(price_str):
    clean_str = price_str.replace("$", "").replace(",", "")

    if clean_str.lower() == "Free":
        clean_str = "0"

    return float(clean_str)


def clean_odometer(odometer_str):
    clean_str = odometer_str.replace("k", "000").replace(",", "").replace(" mi", "")

    return int(clean_str)

CAR_MAKES = [
    "acura",
    "alfa-romeo",
    "aston-martin",
    "audi",
    "bentley",
    "bmw",
    "buick",
    "cadillac",
    "chevrolet",
    "chrysler",
    "dodge",
    "ferrari",
    "fiat",
    "ford",
    "genesis",
    "gmc",
    "honda",
    "hyundai",
    "infiniti",
    "jaguar",
    "jeep",
    "kia",
    "lamborghini",
    "landrover",
    "lexus",
    "lincoln",
    "lucid",
    "maserati",
    "mazda",
    "mclaren",
    "mercedes-benz",
    "mini",
    "mitsubishi",
    "nissan",
    "polestar",
    "porsche",
    "ram",
    "rivian",
    "rolls-royce",
    "subaru",
    "tesla",
    "toyota",
    "volkswagen",
    "volvo",
]


def extract_make(title):
    for make in CAR_MAKES:
        if make in title:
            return make

    return best_fitting_make(title)


def best_fitting_make(title):
    title_words = title.lower().split()
    max_similarity = 0
    best_match = None

    for make in CAR_MAKES:
        similarity = max(SequenceMatcher(None, make, word).ratio() for word in title_words)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = make

    return best_match