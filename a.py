import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# ANSI color codes
GREEN = "\033[92m"
RESET = "\033[0m"

def fetch_data(phone_number):
    url = "https://search5-noneu.truecaller.com/v2/search"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "Authorization": "Bearer a1i03--lnAjzMVW-QwKHIgfiODc9a1_EDVP4K-qCEkPWk1a_GjIA9waN97CLGRef"
    }
    params = {
        "q": phone_number,
        "countryCode": "",
        "type": "4",
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['data']  # Extract the 'data' field from the JSON response
    else:
        return None

def parse_data(data):
    parsed_data = []
    for item in data:
        parsed_item = {}
        parsed_item['name'] = item.get('name', 'N/A')
        parsed_item['gender'] = item.get('gender', 'N/A')
        parsed_item['image'] = item.get('image', 'N/A')
        parsed_item['phones'] = [{'carrier': phone.get('carrier', 'N/A')} for phone in item.get('phones', [])]
        parsed_item['internetAddresses'] = [{'id': address.get('id', 'N/A'), 'service': address.get('service', 'N/A')} for address in item.get('internetAddresses', [])]
        parsed_item['addresses'] = [{'city': address.get('city', 'N/A')} for address in item.get('addresses', [])]
        parsed_data.append(parsed_item)
    return parsed_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    phone_number = request.form['phone_number']
    data = fetch_data(phone_number)
    if data:
        parsed_data = parse_data(data)
        return render_template('result.html', phone_number=phone_number, data=parsed_data)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)