# Taker fees:
# > 0% : 0.25% (0.3% ETC)
# > 1% : 0.24%
# > 2.5% : 0.22%
# > 5% : 0.19%
# > 10% : 0.15%
# > 10% : 0.15%

import requests
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        # self.api_key = api_key
        # self.secret_key = secret_key
        # self.passphrase = passphrase

        self.api_key = '1454684d26a1ac242366170f566f4288'
        self.secret_key = 'Oetkm1ArY/BZCVdOP9JuWW5rkynqMLRG3tvQPPJpCM6GWR8PCElqXTZmdzuKFF7xdwTYDB8vEgBeg04qCGqHjw=='
        self.passphrase = '7yrrrfcur1x'

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = "https://api.gdax.com"
# api_url = "https://api-public.sandbox.gdax.com"

# Authenticate for exchanges
def get_auth(API_KEY, API_SECRET, API_PASS):
  auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)
  return auth

#auth = None
auth = CoinbaseExchangeAuth('1454684d26a1ac242366170f566f4288', 'Oetkm1ArY/BZCVdOP9JuWW5rkynqMLRG3tvQPPJpCM6GWR8PCElqXTZmdzuKFF7xdwTYDB8vEgBeg04qCGqHjw==', '7yrrrfcur1x')

# Return accounts information in JSON format
def get_accounts():
  r = requests.get(api_url + '/accounts', auth=auth)
  return r.json()


# Return order ID in JSON format. You can specify buying by size or by quote currency.
def size_buy(size, product_id):
  order = {
    'size': size,
    'side': 'buy',
    "type": 'market',
    'product_id': product_id
  }
  r = requests.post(api_url + '/orders', json=order, auth=auth)
  return r.json()


# Return order ID in JSON format.
def funds_buy(funds, product_id):
  order = {
      'funds': funds,
      'side': 'buy',
      "type": 'market',
      'product_id': product_id
  }
  r = requests.post(api_url + '/orders', json=order, auth=auth)
  return r.json()

# Return order ID in JSON format. You can specify buying by size or by quote currency.
def size_sell(size, product_id):
  order = {
    'size': size,
    'side': 'sell',
    "type": "market",
    'product_id': product_id
  }
  r = requests.post(api_url + '/orders', json=order, auth=auth)
  return r.json()

# Return order ID in JSON format. You can specify buying by size or by quote currency.
def funds_sell(funds, product_id):
  order = {
      'funds': funds,
      'side': 'sell',
      "type": "market",
      'product_id': product_id
  }
  r = requests.post(api_url + '/orders', json=order, auth=auth)
  return r.json()

# Get a list of all currency pairs for trading.
def get_products():
  r = requests.get(api_url + '/products')
  return r.json()

print get_products()

# Get a list of the best bid and ask orders for a certain product
def get_book(product_id):
  r = requests.get(api_url + '/products/' + product_id + "/book")
  return r.json()

# print repr(get_products())