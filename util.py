import time

# Generate a nonce
def nonce():
  return str(time.time()*1000000)