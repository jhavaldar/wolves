# Taker fees:
# > 0% : 
# > 1% : 
# > 2.5% : 
# > 5% : 
# > 10% : 
# > 10% : 


# Rate Limits



import os
import urllib
import urllib2
import json
import time
import hmac,hashlib


req={}

# Delete this late
APIKey = os.environ('POLO_API')
Secret = os.environ('POLO_SECRET')

command="returnBalances"

#ACCOUNT





#QUOTE
def polo_balance(currencyPair, rate, amount):
  req={}
  req['command'] = 'returnCompleteBalances'
  req['nonce'] = int(time.time()*1000)
  post_data = urllib.urlencode(req)
  sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
  headers = {
      'Sign': sign,
      'Key': APIKey
  }
  ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
  jsonRet = json.loads(ret.read())
  return jsonRet


#BUY
def polo_size_buy(currencyPair, rate, amount):
  req={}
  req['command'] = 'buy'
  req['nonce'] = int(time.time()*1000)
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
def polo_size_sell(currencyPair, rate, amount):
  req={}
  req['command'] = 'sell'
  req['nonce'] = int(time.time()*1000)
  post_data = urllib.urlencode(req)
  sign = hmac.new(Secret, post_data, hashlib.sha512).hexdigest()
  headers = {
      'Sign': sign,
      'Key': APIKey
  }
  ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
  jsonRet = json.loads(ret.read())
  return jsonRet





returnBalances
returnCompleteBalances

buy
sell


print jsonRet

