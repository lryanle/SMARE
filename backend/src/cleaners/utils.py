def clean_currency(price_str):
    clean_str = price_str.replace("$", "").replace(",", "")

    if clean_str.lower() == "Free":
        clean_str = "0"

    return float(clean_str)


def clean_odometer(odometer_str):
    clean_str = odometer_str.replace("k", "000").replace(",", "").replace(" mi", "")

    return int(clean_str)
