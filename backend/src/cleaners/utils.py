def cleanCurrency(priceStr):
    cleanStr = priceStr.replace("$", "").replace(",", "")

    if cleanStr.lower() == "Free":
        cleanStr = "0"

    return float(cleanStr)
