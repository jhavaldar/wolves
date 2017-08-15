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


import requests
import os
import urllib
import urllib2
import json
import time
import hmac,hashlib

req={}

# Delete this late
api_file = open("api_polo.txt", "r")
API = api_file.readlines()

# API KEYS
APIKey = API[0].rstrip()
Secret = API[1]


#ACCOUNT


#QUOTE - specific current pair
#{"asks":[[0.00007600,1164],[0.00007620,1300], ... ], "bids":[[0.00006901,200],[0.00006900,408], ... ], "isFrozen": 0, "seq": 18849}
def polo_quote(currencyPair):
  ret = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair='+currencyPair+'&depth=10')
  return ret.json()


#BALANCE
#{u'available': u'0.00000000', u'onOrders': u'0.00000000', u'btcValue': u'0.00000000'}
def polo_balance(coin):
  req={}
  req['command'] = 'returnCompleteBalances'
  req['nonce'] = int(time.time()*1000)
  req['account'] = 'all'
  post_data = urllib.urlencode(req)
  sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
  headers = {
      'Sign': sign,
      'Key': APIKey
  }
  ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
  jsonRet = json.loads(ret.read())
  return jsonRet[coin]



#BUY
# {"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173","total":"0.00058625","tradeID":"16164","type":"buy"}]}
def polo_size_buy(currencyPair, rate, amount):
  req={}
  req['command'] = 'buy'
  req['nonce'] = int(time.time()*1000)
  req['currencyPair'] = currencyPair
  req['rate'] = rate
  req['amount'] = amount
  post_data = urllib.urlencode(req)
  sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
  headers = {
      'Sign': sign,
      'Key': APIKey
  }
  ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
  jsonRet = json.loads(ret.read())
  return jsonRet



#SELL
# {"orderNumber":31226040,"resultingTrades":[{"amount":"338.8732","date":"2014-10-18 23:03:21","rate":"0.00000173","total":"0.00058625","tradeID":"16164","type":"sell"}]}
def polo_size_sell(currencyPair, rate, amount):
  req={}
  req['command'] = 'sell'
  req['nonce'] = int(time.time()*1000)
  req['currencyPair'] = currencyPair
  req['rate'] = rate
  req['amount'] = amount
  post_data = urllib.urlencode(req)
  sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
  headers = {
      'Sign': sign,
      'Key': APIKey
  }
  ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
  jsonRet = json.loads(ret.read())
  return jsonRet



# BTC_SC

# returnBalances
# returnCompleteBalances

# buy
# sell


