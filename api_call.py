from datetime import datetime
import requests
from Kryptosteuertool.secret import api_key


def get_price_of_currency(date, src_currency, dst_currency, exchange_name):
    if src_currency == 'XBT':
        src_currency = 'BTC'
    if dst_currency == 'XBT':
        dst_currency = 'BTC'
    url = 'https://min-api.cryptocompare.com/data/v2/histohour?toTs=' + datetime.strptime(date,
                                                                                          '%Y-%m-%d %H:%M:%S').strftime(
        '%s') + '&e=' + exchange_name + '&fsym=' + src_currency + '&tsym=' + dst_currency + '&limit=1&api_key=' + api_key
    try:
        data = requests.get(url).json()['Data']['Data']
        price = (float(data[0]['close']) + float(data[1]['close'])) / 2
        return price
    except:
        print('API unsuccessfully!')
        return -1
