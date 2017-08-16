# Taker fees:
# < 600 BTC : 0.25% 
# > 600 BTC : 0.24% 
# >= 1200 BTC : 0.22% 
# >= 2400 BTC : 0.20% 
# >= 6000 BTC : 0.16% 
# >= 12,000 BTC : 0.14% 
# >= 18,000 BTC : 0.12% 
# >= 24,000 BTC : 0.10% 
# >= 60,000 BTC : 0.08% 
# >= 120,000 BTC : 0.05% 

# Taker fees:
# < 600 BTC : 0.15% 
# > 600 BTC : 0.14% 
# >= 1200 BTC : 0.12% 
# >= 2400 BTC : 0.10% 
# >= 6000 BTC : 0.08% 
# >= 12,000 BTC : 0.05% 
# >= 18,000 BTC : 0.02% 
# >= 24,000 BTC : 0% 
# >= 60,000 BTC : 0% 
# >= 120,000 BTC : 0% 


# Rate Limits
# 6 call/second

import requests, os, hmac, hashlib, json, base64
from requests.auth import AuthBase
import util
import numpy as np

# Create custom authentication for exchange
class PoloniexExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
      data = json.dumps(request)
      h = hmac.new(self.secret_key, data, hashlib.sha512)
      signature = h.hexdigest()

      request.headers.update({
        "Sign": signature,
        "Key": self.api_key
      })
      return request

api_file = "api_polo.txt"

# Get the API Key and the API Secret
def get_auth(api_file):
  with open(api_file, 'r') as file:
    arr = file.read().split("\n")
    API_KEY = arr[0]
    API_SECRET = arr[1]
    auth = PoloniexExchangeAuth(API_KEY, API_SECRET)
    return auth

auth = get_auth(api_file)

endpoint_url = 'https://poloniex.com/tradingApi'

# Get bidding/asking price, over the last 10 bids/asks
# Highest ask and lowest bid; worst case scenario.
# side = 'bids' or 'asks'
def get_rate(currencyPair, side):
  if side not in ['asks', 'bids']:
    raise Exception("Invalid side for transaction.")
  orders = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair='+currencyPair+'&depth=10').json()
  print orders
  prices = [float(order[0]) for order in orders[side]]
  amounts = [float(order[1]) for order in orders[side]]
  zipped = zip(prices, amounts)
  rates = [d[1]/d[0] for d in zipped]
  if side=='asks':
    return np.amax(rates)
  if side=='bids':
    return np.amin(rates)

# Returns the balance in each currency, in JSON format
#{u'available': u'0.00000000', u'onOrders': u'0.00000000', u'btcValue': u'0.00000000'}
def get_balance(coin):
  order = {
    'command': 'returnCompleteBalances',
    'nonce': util.nonce(),
    'account': 'all'
  }
  r = requests.post(endpoint_url, data=order, auth=auth).json()
  if 'error' in r:
    raise Exception("Request Error: " + r['error'])
  if coin not in r:
    raise Exception("No coin with that name.")
  return r[coin]

# Buy/sell, with product_id being the currency pair. Returns response in JSON format.
# {"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173","total":"0.00058625","tradeID":"16164","type":"buy"}]}
def place_order(currencyPair, rate, amount, side):
  if side not in ['buy', 'sell']:
    raise Exception("Invalid side for transaction.")
  order = {
    'command': side,
    'nonce': util.nonce(),
    'currencyPair': currencyPair,
    'rate': rate,
    'amount': amount,
    'immediateOrCancel': 1
  }
  r = requests.post(endpoint_url, data=order, auth=auth)
  if 'error' in r:
    raise Exception("Request Error: " + r['error'])
  return r

# Margin uy/sell, with product_id being the currency pair. Returns response in JSON format.
# {"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173","total":"0.00058625","tradeID":"16164","type":"buy"}]}
def place_margin_order(currencyPair, rate, amount, side):
  if side not in ['buy', 'sell']:
    raise Exception("Invalid side for transaction.")
  command = 'marginBuy'
  if side == 'sell':
    command = 'marginSell'
  order = {
    'command': command,
    'nonce': util.nonce(),
    'currencyPair': currencyPair,
    'rate': rate,
    'amount': amount,
    'immediateOrCancel': 1
  }
  r = requests.post(endpoint_url, data=order, auth=auth)
  if 'error' in r:
    raise Exception("Request Error: " + r['error'])
  return r

print get_rate('BTC_LTC', 'asks')
print get_rate('BTC_LTC', 'bids')