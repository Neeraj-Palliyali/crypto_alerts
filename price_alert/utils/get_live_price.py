import requests
import json


def get_live_price_btc():
    url  = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    response = requests.get(url=url)
    data = json.loads(response.text)
    for i in data:
        if i.get('id') == 'bitcoin':
            return i.get('current_price')
        else:
            return False