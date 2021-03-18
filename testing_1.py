import requests
import json
from pprint import pprint
import time
import datetime
import asyncio
import aiohttp


# response = requests.get('https://api.blockchain.com/v3/exchange/l3/BTC-USDT')
# response_3 = json.loads(response.content)
# print(response['asks'][0], response['bids'][0])
# print(len(response['asks']), len(response['bids']))
# pprint(response['asks'])
# response = requests.get('https://api.blockchain.com/v3/exchange/l2/ETH-USDT')
# response_2 = json.loads(response.content)
# # print(response['asks'][0], response['bids'][0])
# if 'asks' in response_2:
#     pprint(response_2)

# other links
# 'https://api.exmo.com/v1.1/order_book?pair=BTC_USDT&limit=5',
# elif 'exmo' in i:
#     ask_list['exmo'] = float(data_list[i]['BTC_USDT']['ask'][0][0])
#     bid_list['exmo'] = float(data_list[i]['BTC_USDT']['bid'][0][0])
    # print('ask', data_list[i]['BTC_USDT']['ask'][0], 'bid', data_list[i]['BTC_USDT']['bid'][0])

# 'https://okex.com/api/v5/market/books?instId=BTC-USDT&sz=5',
# elif 'okex' in i:
#     try:
#         if data_list[i]['data'][0]['asks']:
#             ask_list['okex'] = float(data_list[i]['data'][0]['asks'][0][0])
#     except:
#         pass
#     bid_list['okex'] = float(data_list[i]['data'][0]['bids'][0][0])
    # print('ask', data_list[i]['data'][0]['asks'][0], 'bid', data_list[i]['data'][0]['bids'][0])

# 'https://cex.io/api/order_book/BTC/USDT/?depth=5',
# elif 'cex' in i:
#     ask_list['cex'] = float(data_list[i]['asks'][0][0])
#     bid_list['cex'] = float(data_list[i]['bids'][0][0])
    # print('ask', data_list[i]['asks'][0], 'bid', data_list[i]['bids'][0])

# 'https://api.hitbtc.com/api/2/public/orderbook',
# elif 'hitbtc' in i:
#     ask_list['hitbtc'] = float(data_list[i]['BTCUSD']['ask'][0]['price'])
#     bid_list['hitbtc'] = float(data_list[i]['BTCUSD']['bid'][0]['price'])
    # print('ask', data_list[i]['BTCTUSD']['ask'][0], 'bid', data_list[i]['BTCTUSD']['bid'][0])

# print(((48006.38 * 0.09999) - (47703.32 * 0.09999)) - (((48006.38 * 0.09999 * 0.16) / 100) + ((47703.32 * 0.09999 * 0.15) / 100)))
# 26.424912592487658
# Bitmex APi https://www.bitmex.com/api/explorer/#!/OrderBook/OrderBook_getL2
# proxy = {"https": "https://194.254.119.2:80"}
# pprint(requests.get('https://www.bitmex.com/api/v1/orderBook/L2?symbol=LINKUSDT&depth=25', proxies=proxy))

# pprint(requests.get('https://api.kraken.com/0/public/Depth?pair=LINKUSDT').json())

# Coinbase API https://docs.pro.coinbase.com/#get-product-order-book
# pprint(requests.get('https://api.pro.coinbase.com/products/BTC-USDC/book?level=2').json())



# pprint(requests.get('https://api.kraken.com/0/public/Depth?pair=BTCUSDC').json())
# pprint(requests.get('https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0').json())



# ALKO testing
# response = requests.get('https://alko.www-technologies.ru/api/orders')
#
# print(response.json())
#
# params = {"order_id": 36,
#           "status": 0,
#           "remove": [
#               {
#                 "item_id": 4193471,
#                 "quantity": 2
#               }
#                     ],
#           "add": []}
# response_edit = requests.post('https://alko.www-technologies.ru/api/order/36', params=params)
# print(response_edit)




import websocket

# socket = "wss://www.bitmex.com/realtime"
# socket = "wss://www.bitmex.com/realtime?subscribe=orderBookL2_25:LINKUSDT"
# socket = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"
#
#
# def on_open(ws):
#     print('Opened')
#
#
# def on_ping(ws):
#     print('ping')
#
#
# def on_message(ws, messsage):
#
#     print(messsage)


# params = {
# "method": "SUBSCRIBE",
# "params":
# [
# "btcusdt@aggTrade",
# "btcusdt@depth"
# ],
# "id": 1
# }
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_ping=on_ping)
# ws.run_forever()
# ws.send(params)


# while True:
#     start = time.time()
    # response = requests.get('https://api.huobi.pro/market/depth?symbol=linkusdt&type=step1').json()
    # response = requests.get('https://global-openapi.bithumb.pro/market/data/orderBook?symbol=BTC-USDT').json()
    # response = requests.get('https://global-openapi.bithumb.pro/market/data/orderBook?symbol=ETH-USDT').json()
    # response = requests.get('https://global-openapi.bithumb.pro/market/data/orderBook?symbol=LTC-USDT').json()
    # response = requests.get('https://ru.bitstamp.net/api/v2/order_book/btcusdc/').json()
    # print(time.time() - start)
    # pprint(response)
    # break




# testing futures

# kraken = 53000
# kraken_volume = 1
# binance = 54000
# binance_volume = kraken * kraken_volume / binance
# # binance_volume = 1
# print(binance * binance_volume)
# while True:
#     kraken_price = int(input('Kraken price'))
#     binance_price = int(input('Binance price'))
#     # kraken_profit = kraken_volume * kraken_price - kraken * kraken_volume
#     kraken_profit = kraken * kraken_volume - kraken_volume * kraken_price
#     # binance_profit = binance * binance_volume - binance_volume * binance_price
#     binance_profit = binance_volume * binance_price - binance * binance_volume
#     print('Kraken profit', kraken_profit, 'Binance profit', binance_profit)
#     # print(kraken_profit + binance_profit)
#     # print('total profit', (kraken + binance) - ((kraken + binance) + (kraken_profit + binance_profit)))


# long = 0
# short = 0
# max_profit = 0
# # futures
# while True:
#     ask_list = {}
#     bid_list = {}
#     binance = requests.get('https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10').json()
#     bybit = requests.get('https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSDT').json()
#     keyfunc = lambda x: x['price']
#     bids = [i for i in bybit['result'] if i['side'] == 'Buy']
#     bids.sort(key=keyfunc)
#     asks = [i for i in bybit['result'] if i['side'] == 'Sell']
#     asks.sort(key=keyfunc)
#     if asks:
#         ask_list['bybit'] = []
#         ask_list['bybit'].append(float(asks[-1]['price']))
#         ask_list['bybit'].append(float(asks[-1]['size']))
#     if bids:
#         bid_list['bybit'] = []
#         bid_list['bybit'].append(float(bids[-1]['price']))
#         bid_list['bybit'].append(float(bids[-1]['size']))
#
#     ask_list['binance'] = []
#     ask_list['binance'].append(float(binance['asks'][0][0]))
#     ask_list['binance'].append(float(binance['asks'][0][1]))
#
#     bid_list['binance'] = []
#     bid_list['binance'].append(float(binance['bids'][0][0]))
#     bid_list['binance'].append(float(binance['bids'][0][1]))
#
#     # short_platform = None
#     # long_platform = None
#     if not long and not short:
#         # long = ask_list['bybit'][0]
#         # short = bid_list['bybit'][0]
#         # short = bid_list['binance'][0]
#         # long = ask_list['binance'][0]
#         if bid_list['bybit'][0] > ask_list['binance'][0]:
#             short = bid_list['bybit'][0]
#             short_platform = 'bybit'
#             long = ask_list['binance'][0]
#             long_platform = 'binance'
#         else:
#             long = ask_list['bybit'][0]
#             long_platform = 'bybit'
#             short = bid_list['binance'][0]
#             short_platform = 'binance'
#
#         print(long_platform, 'long', long, short_platform, 'short', short)
#         # print(ask_list, bid_list)
#
#     # long_profit = bid_list['bybit'][0] - long
#     long_profit = bid_list[long_platform][0] - long
#     # short_profit = short - ask_list['binance'][0]
#     short_profit = short - ask_list[short_platform][0]
#
#     total_profit = long_profit + short_profit
#
#     # if total_profit > 0:
#     #     if max_profit < total_profit:
#     #         max_profit = total_profit
#     #     print(f'long profit {long_profit}, short profit {short_profit}, total profit {total_profit}, max profit {max_profit}')
#
#     if total_profit > 15:
#         # if max_profit < total_profit:
#         #     max_profit = total_profit
#         max_profit += total_profit
#         print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
#         long = 0
#         short = 0

# async futures test
links = [
         'https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10',
         'https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT'
         ]

data_list = dict()


async def get_content(url, session):
    async with session.get(url) as response:
        try:
            data = await response.read()
            data = json.loads(data)
            data_list[url] = data
        except:
            print(url)


async def main():

    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        for i in links:
            try:
                task = asyncio.create_task(get_content(i, session))
                tasks.append(task)
            except:
                pass
        try:
            await asyncio.gather(*tasks)
        except:
            pass

max_profit = 0
long = 0
short = 0

while True:
    start = time.time()
    asyncio.run(main())
    ask_list = dict()
    bid_list = dict()
    for i in data_list:
        if i == 'https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10':
            ask_list['binance'] = []
            ask_list['binance'].append(float(data_list[i]['asks'][0][0]))
            ask_list['binance'].append(float(data_list[i]['asks'][0][1]))

            bid_list['binance'] = []
            bid_list['binance'].append(float(data_list[i]['bids'][0][0]))
            bid_list['binance'].append(float(data_list[i]['bids'][0][1]))

        elif i == 'https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSDT':
            keyfunc = lambda x: x['price']
            bids = [i for i in data_list[i]['result'] if i['side'] == 'Buy']
            bids.sort(key=keyfunc)
            asks = [i for i in data_list[i]['result'] if i['side'] == 'Sell']
            asks.sort(key=keyfunc)
            if asks:
                ask_list['bybit'] = []
                ask_list['bybit'].append(float(asks[-1]['price']))
                ask_list['bybit'].append(float(asks[-1]['size']))
            if bids:
                bid_list['bybit'] = []
                bid_list['bybit'].append(float(bids[-1]['price']))
                bid_list['bybit'].append(float(bids[-1]['size']))

    if not long and not short:
        if bid_list['bybit'][0] > ask_list['binance'][0]:
            short = bid_list['bybit'][0]
            short_platform = 'bybit'
            long = ask_list['binance'][0]
            long_platform = 'binance'
        else:
            long = ask_list['bybit'][0]
            long_platform = 'bybit'
            short = bid_list['binance'][0]
            short_platform = 'binance'

        print(long_platform, 'long', long, short_platform, 'short', short, 'time', datetime.datetime.now())

    fees = {'binance': 0.04, 'bybit': 0.075}
    long_profit = bid_list[long_platform][0] - long
    short_profit = short - ask_list[short_platform][0]
    total_profit = long_profit + short_profit
    clear_profit = total_profit - ((long * fees[long_platform] / 100) + (short * fees[short_platform] / 100))
    # print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию , time {datetime.datetime.now()}')
    # print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, clear profit {clear_profit}, Прибыль за сессию , time {datetime.datetime.now()}')
    # print(time.time() - start)
    # if total_profit > 80:
    if clear_profit > 0:
        max_profit += clear_profit
        print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, clear profit {clear_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
        long = 0
        short = 0

# print(requests.get('https://api-futures.kucoin.com/api/v1/level2/depth20?symbol=XBTUSDM').json())
# print(requests.get('https://api.hbdm.com/market/depth?symbol=BTC').json())


# print(requests.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=5').json())
# print(requests.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step0").json())
# print(requests.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step1").json())
# print(requests.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step2").json())
# print(requests.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step3").json())
# print(requests.get("https://api.huobi.pro/market/depth?symbol=btcusdt&type=step4").json())
# pprint(requests.get("https://vapi.binance.com/vapi/v1/exchangeInfo").json())

# response = requests.get("https://vapi.binance.com/vapi/v1/exchangeInfo").json()
# response = requests.get("https://testnet.binanceops.com/vapi/v1/exchangeInfo").json()
# start_time = response['data']['serverTime']
# calls = [i for i in response['data']['optionSymbols'] if i['side'] == 'CALL']
# puts = [i for i in response['data']['optionSymbols'] if i['side'] == 'PUT']
# for i in calls:
#     i['expiryDate'] = i['expiryDate'] - time.time()
# print(calls)
# for i in puts:
#     i['expiryDate'] = i['expiryDate'] - time.time()
# print(puts)
# print(start_time)
# print(response['data']['optionSymbols'])
# pprint(requests.get("https://vapi.binance.com/vapi/v1/depth?symbol=BTC-210326-52000-C").json())
# print(time.time())


# Bithumb API https://github.com/bithumb-pro/python-api-client/blob/master/BithumbGlobal.py
# print(requests.get('https://global-openapi.bithumb.pro/market/data/orderBook?symbol=LTC-USDT').json())

# depth test
# print(requests.get('https://api.huobi.pro/market/depth?symbol=btcusdt&type=step0').json())
# print(requests.get('https://api.huobi.pro/market/depth?symbol=btcusdt&type=step1').json())
# right
# print(requests.get('https://api.huobi.pro/market/depth?symbol=btcusdt&type=step2').json())
# print(requests.get('https://api.huobi.pro/market/depth?symbol=btcusdt&type=step3').json())

# print(requests.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10').json())
# print(requests.get('https://api.kraken.com/0/public/Depth?pair=BTCUSDT').json())
# print(requests.get('https://api.kraken.com/0/public/Depth?pair=XBTUSDT').json())
# right
# print(requests.get('https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol=BTC-USDT').json())
# right
# print(requests.get('https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0').json())
# print(requests.get('https://global-openapi.bithumb.pro/market/data/orderBook?symbol=BTC-USDT').json())
# print(requests.get('https://global-openapi.bithumb.pro/openapi/v1/spot/orderBook?symbol=BTC-USDT').json())
# print(requests.get('https://api.crypto.com/v2/public/get-book?instrument_name=LINK_USDT&depth=10').json())

