import ccxt
#print(ccxt.exchanges)
kucoin=ccxt.kucoin()
btc_price=kucoin.fetch_ticker('BTC/USDT')
print(btc_price['last'])