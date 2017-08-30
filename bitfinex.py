# Rate Limits: <60 requests per minute
# Taker Fees
# $0.00 or more traded  0.20%
# $500,000.00 or more traded  0.20%
# $1,000,000.00 or more traded  0.20%
# $2,500,000.00 or more traded  0.20%
# $5,000,000.00 or more traded  0.20%
# $7,500,000.00 or more traded  0.20%
# $10,000,000.00 or more traded 0.18%
# $15,000,000.00 or more traded 0.16%
# $20,000,000.00 or more traded 0.14%
# $25,000,000.00 or more traded 0.12%
# $30,000,000.00 or more traded 0.10%
  
# Maker Fees
# $0.00 or more traded  0.10%
# $500,000.00 or more traded  0.08%
# $1,000,000.00 or more traded  0.06%
# $2,500,000.00 or more traded  0.04%
# $5,000,000.00 or more traded  0.02%
# $7,500,000.00 or more traded  0.00%
# $10,000,000.00 or more traded 0.00%
# $15,000,000.00 or more traded 0.00%
# $20,000,000.00 or more traded 0.00%
# $25,000,000.00 or more traded 0.00%
# $30,000,000.00 or more traded 0.00%

import requests
import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from random import randint
import numpy as np

endpoint_url = 'https://api.bitfinex.com/v1'

# Generate a nonce
def nonce():
  return str(time.time()*1000)

# Signs the payload of a request
def sign_payload(payload):
  j = json.dumps(payload)
  data = base64.standard_b64encode(j.encode('utf8'))

  h = hmac.new(API_SECRET.encode('utf8'), data, hashlib.sha384)
  signature = h.hexdigest()
  return {
      "X-BFX-APIKEY": API_KEY,
      "X-BFX-SIGNATURE": signature,
      "X-BFX-PAYLOAD": data
  }

# Get all the currency pair IDs
def symbols():
  r = requests.get(endpoint_url + "/symbols", verify=True)
  rep = r.json()
  return rep

# Symbol is the currency pair you're trading. Amount is size. For a market order, use a random number.
# The order type is 'market', 'limit', or others.
def place_order(size, price, side, ord_type, symbol, exchange='bitfinex'): # submit a new order.

  payload = {
    "request":"/v1/order/new",
    "nonce":nonce(),
    "symbol":symbol,
    "amount":size,
    "price":price,
    "exchange":exchange,
    "side":side,
    "type":ord_type
  }

  signed_payload = sign_payload(payload)
  r = requests.post(endpoint_url + "/order/new", headers=signed_payload, verify=True)
  rep = r.json()

  try:
    rep['order_id']
  except:
    return rep['message']

  return rep

# Buy a symbol at a size (market order)
def buy(size, symbol):
  place_order(size, randint(0, 1000), 'buy', 'market', symbol)

# Buy a symbol at a size (market order)
def sell(size, price, symbol):
  place_order(size, randint(0, 1000), 'sell', 'market', symbol)

# Get the 10 most recent asks and bids from the order book
def get_orders(symbol):
  r = requests.get(endpoint_url + "/book/" + symbol, data={'limit_bids':'10', 'limit_asks':'10'}, verify=True)
  return json.loads(r.text)

# Get average bidding/asking price, over the last 10 bids/asks
# side = 'bids' or 'asks'
def get_rate(symbol, side):
  if side not in ['asks', 'bids']:
    print "Wrong format for 'side' parameter"
    return -1
  prices = [float(order['price']) for order in get_orders(symbol)[side]]
  amounts = [float(order['amount']) for order in get_orders(symbol)[side]]
  zipped = zip(prices, amounts)
  rates = [d[0]/d[1] for d in zipped]
  if side=='asks':
    return np.amax(rates)
  if side=='bids':
    return np.amin(rates)

# Get the API Key and the API Secret
def get_auth():
  with open('api_bitfinex.txt', 'r') as file:
    arr = file.read().split("\n")
    return arr[0], arr[1]

API_KEY, API_SECRET = get_auth()

print sell(1.0, 100, "ltcusd")


