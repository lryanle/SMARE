import re


def cleanCurrency(priceStr):
    cleanStr = priceStr.replace("$", "").replace(",", "")

    if cleanStr.lower() == "Free":
        cleanStr = "0"

    return float(cleanStr)


def cleanOdometer(odometerStr):
    cleanStr = odometerStr.replace("k", "000").replace(",", "").replace(" mi", "")

    return int(cleanStr)