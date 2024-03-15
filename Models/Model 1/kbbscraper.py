from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)


# Function to scrape current market price from Kelly Blue Book
def get_kbb_price(make, model, year):
    base_url = f'https://www.kbb.com/{make}/{model}/{year}'
    try:
        response = requests.get(base_url)

        # Use regular expression to extract the price information
        pattern = re.compile(r'"nationalBaseDefaultPrice":(\d+),')
        match = pattern.search(response.text)
        
        kbb_price = match.group(1) if match else None
        return kbb_price
    
    except Exception as e:
        return None
print()
@app.route('/get_price', methods=['GET'])
def price_endpoint():
    make = request.args.get('make')
    model = request.args.get('model')
    year = request.args.get('year')
    price = get_kbb_price(make, model, year)
    return jsonify({'price': price})

if __name__ == '__main__':
    app.run(debug=True)
