from binance.client import Client
from binance.enums import *
import requests


# api_key = 'qqMreehNqD4UwGtQXTToBZnahEOxT1iwFX43wWpFpewohGml8mp0lrmptC5w1WdS'
# api_secret = 'DDUWksXWi3G7W877Dka5L8DP7EF3rvys6mn5l236bFrdZ5ojKWI6xntjS86cCaF7'
# api_key = 'OZFcVN2cEgocii36tNniPGg9pcVDuWL8tbUdA3Aa3vyp0jG3kDs0VD9EQcXVWt67'
# api_secret = 'gT7VX0LjRuPaSi7BZcms4vwp5B0envjkAylZSgC5N3P9K68PWjzwioJsrT4VaF0u'
# client = Client(api_key, api_secret)
#
# info = client.get_account()
# print(info)
# print(client.futures_account())
# print(client.get_sub_account_list())
# for i in info:
#     print(i)

# order = client.create_order(
#     symbol='BTCUSDT',
#     side=SIDE_SELL,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=100,
#     price='60000')
#
# print(order)
# https://api1.binance.com
# print(requests.get('https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT').json())
from pprint import pprint
import time
# while True:
#     start = time.time()
# #     print(requests.get('https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT').json())
#     r = requests.get('https://api.aax.com/v2/market/orderbook?symbol=BTCUSDTFP&level=20').json()
#     pprint(time.time() - start)
    # bid = r['result'][0]['bid_price']
    # ask = r['result'][0]['ask_price']
    # print('ask', ask, 'bid', bid)

# works
# import websocket
#
# ws = websocket.WebSocket()
# ws.connect("wss://realtime.aax.com/marketdata/v2/")
# ws.send('{"e": "subscribe", "stream": "BTCUSDT@book_50"}')
# while True:
#     print("Received '%s'" % ws.recv())




