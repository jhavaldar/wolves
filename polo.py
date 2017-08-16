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


import requests, os, time, hmac, hashlib, json, base64
import urllib, urllib2
from requests.auth import AuthBase

# Delete this late
api_file = open("api_polo.txt", "r")
API = api_file.readlines()

# API KEYS
API_KEY = API[0].rstrip()
API_SECRET = API[1]

# Generate a nonce
def nonce():
  return str(time.time()*1000)

# Create custom authentication for Exchange
class PoloniexExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
      data = request.body
      h = hmac.new(API_SECRET, data, hashlib.sha512)
      signature = h.hexdigest()

      request.headers.update({
        "Sign": signature,
        "Key": self.api_key
      })
      return request

# Returns an authenticated object for the exchange.
def get_auth(API_KEY, API_SECRET):
  auth = PoloniexExchangeAuth(API_KEY, API_SECRET)
  return auth

auth = get_auth(API_KEY, API_SECRET)

endpoint_url = 'https://poloniex.com/tradingApi'

#QUOTE - specific current pair
#{"asks":[[0.00007600,1164],[0.00007620,1300], ... ], "bids":[[0.00006901,200],[0.00006900,408], ... ], "isFrozen": 0, "seq": 18849}
def polo_quote(currencyPair):
  r = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair='+currencyPair+'&depth=10')
  return r.json()

# Returns the balance in each currency, in JSON format
#{u'available': u'0.00000000', u'onOrders': u'0.00000000', u'btcValue': u'0.00000000'}
def polo_balance(coin):
  order = {
    'command': 'returnCompleteBalances',
    'nonce': nonce(),
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
def order(currencyPair, rate, amount, side):
  if side not in ['buy', 'sell']:
    raise Exception("Invalid side for transaction.")
  order = {
    'command': side,
    'nonce': nonce(),
    'currencyPair': currencyPair,
    'rate': rate,
    'amount': amount
  }
  r = requests.post(endpoint_url, data=order, auth=auth)
  if 'error' in r:
    raise Exception("Request Error: " + r['error'])
  return r
