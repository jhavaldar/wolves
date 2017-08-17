from gdax import get_accounts, size_buy, funds_buy, size_sell, funds_sell, get_products, get_book
from polo import polo_quote, polo_balance, polo_size_buy, polo_size_sell
from bitfinex import buy, sell, get_orders, get_rate

import copy

EXCHANGES = {'bitfinex', 'poloniex', 'gdax'}

FEES = {
  'bitfinex': 0.025,
  'poloniex': 0.025,
  'gdax': 0.025
}

PRODUCTS = {
  'LTC-BTC',
  'ETH-BTC',
  'ETH-BTC',
  'ETH-BTC',
  'ETH-BTC',


}

# Buy long from an exchange. size is the amount of currency, exchanges are listed above
# and product is the currency pair being traded.
def buy_long(size, exchange, product):
  return {'gdax': size_buy(),
   'polo': polo_size_buy(),
   'bitfinex': buy()}[exchange]()
  # stubbity stub
  return

# Buy short from an exchange. size is the amount of currency, exchanges are listed above
# and product is the currency pair being traded.
def buy_short(size, exchange, product):
  return {'gdax': buy_short(),
   'polo': polo_size_buy_short(),
   'bitfinex': buy_short()}[exchange]()
  # stubbity stub
  return

# Sell long from an exchange. size is the amount of currency, exchanges are listed above
# and product is the currency pair being traded.
def sell_long(size, exchange, product):
  return {'gdax': size_sell(),
   'polo': polo_size_sell(),
   'bitfinex': sell()}[exchange]()
  # stubbity stub
  return

# Sell short from an exchange. size is the amount of currency, exchanges are listed above
# and product is the currency pair being traded.
def sell_short(size, exchange, product):
  return {'gdax': sell_short(),
   'polo': polo_size_sell_short(),
   'bitfinex': sell_short()}[exchange]()
  # stubbity stub
  return

# Get the rates for a product in a given exchange.
def get_rate(exchange, product):
  # return {'gdax': (),
  #  'polo': (),
  #  'bitfinex': ()}[exchange]()
  # stubbity stub
  return

######## Write these functions using the above functions and add more stubs if you need them.

# Write a function to check for arbitrage.
# Return the two exchanges, in order of lowest to highest rate, and the currency pair we will trade.

# Bitcoin
# COINS ON POLO AND BITFINNEX
# Dash
# Ethereum
# Litecoin
# Ripple
# Bitcoin Cash
# Monero
# Ethereum Classic
# Zcash

#COINS on GDAX
# Ethereum
# Litecoin

# LIST OF EXCHANGES
exchange_list = ['gdax', 'polo', 'bitfinex']
alt_exchange_list=['polo', 'bitfinex']

# LIST OF COINS
basic_coins = []
alt_coins = []


def check_for_arbitrage():
  #for each coin, compare each exchange
  basic_opps=compare_exchanges(exchange_list, basic_coins)
  alt_opps=compare_exchanges(alt_exchange_list, alt_coins)
  return basic_opps if basic_opps['diff'] > alt_opps['diff'] else alt_opps
  
  #output a coin, and exchanges in a dictionary with coin: , low: , high: , diff:

def compare_exchanges(exchanges, coins):
  #GIVEN list of exhcnages, and relevant coins to each ones in array format
  #Return best
  opps={}
  compare={'coin': x};
  for x in coins:  
    compare={exchange:get_rate(exchanges,coin) for exchange in exchanges}
    comparison = compare_rates(compare)
    if comparison['diff'] > opps['diff']:
      opps = copy.deepcopy(comparison)


  #OLD CODE
  # for x in coins:
  #   compare={'coin': x};
  #   for y in exchanges:
  #     compare[y] = get_rate(y, x)
  #   comparison = compare_rates(compare)
  #   if comparison['diff'] > opps['diff']:
  #     opps = copy.deepcopy(comparison)
  return opps

def compare_rates(rates_dict):
  #GIVEN dictionary with 'coin' and exchanges associated with their rates of that coin
  #Return highest arbitrage opportunity between the exchanges as a 'coin', 'exchange_low', 'exchange_high', 'diff'
  # Stubbity stub



# Write a function to check if we can actually make a profit trading at a given size. (return true or false)
# Maybe later on, we can check what size and final_spread we need to be at to make a profit.
# Use the "FEES" variable above
def should_enter_market(size, exit_spread):
  # Stubbity stub
  return False

# Write a function to enter the market.
def enter_market():
  # Stubbity stub
  return

# Write a function to exit the market.
def exit_market():
  # Stubbity stub
  return

# Write a function to log data to file. You should do this after every action.
def log_to_file():
  # Stubbity stub
  return

# Here is an example function which calculates profits from a trade.
# p is the intiial price of the asset in the lower market
# trade_fee is the fee (assumed to be the same for each order)
# epsilon is the % spread when we enter the market.
# delta is the % spread when exit the market.
# u is the change in the asset's price between entering and exiting the market.
# size is the amount of asset traded.
def do_trade(p, trade_fee, delta, epsilon, u, size=1):
  A_fiat = 0  #Initial fiat in A
  A_asset = 0 #Initial asset in A
  B_fiat = 0  #Initial fiat in B
  B_asset = 0 #Initial asset in B

  # Do the first trade: short-sell A at price p*(1+epsilon), buy long in B
  A_fiat += (size*p*(1+ epsilon))*(1 - trade_fee)
  A_asset -= size
  B_fiat -= (size*p)*(1 + trade_fee)
  B_asset += size

  arr = [[A_fiat, A_asset],[B_fiat, B_asset]]

  # Do the second trade: sell B at price (p + u)
  #  buy back A at price (p+u)*(1+delta)
  A_fiat -= (size*(p+u)*(1+delta))*(1 + trade_fee)
  A_asset += size
  B_fiat += (size*(p+u))*(1 - trade_fee)
  B_asset -= size

  arr = [[A_fiat, A_asset],[B_fiat, B_asset]]
  return A_fiat+B_fiat
