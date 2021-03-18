import requests
import json
from pprint import pprint
import time
import datetime
import asyncio
import aiohttp
import websocket

ws = websocket.WebSocket()
aax_url = "wss://realtime.aax.com/marketdata/v2/"
ws.connect(aax_url)
ws.send('{"e": "subscribe", "stream": "BTCUSDTFP@book_50"}')
ws.recv()
ws.recv()
ws.recv()

links = [
         'https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT',
         # 'https://www.binance.com'
         ]

data_list = dict()


async def get_content(url, session):
    async with session.get(url) as response:
        # if url == 'https://www.binance.com':
        #     data_list[aax_url] = json.loads(ws.recv())

        # else:
        try:
            data = await response.read()
            data = json.loads(data)
            data_list[url] = data

            # data_list[aax_url] = ws.recv()
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
    # print(data_list)
    data_list[aax_url] = json.loads(ws.recv())
    for i in data_list:
        if i == 'https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT':
            ask_list['binance'] = []
            ask_list['binance'].append(float(data_list[i]['askPrice']))
            # ask_list['binance'].append(float(data_list[i]['asks'][0][1]))

            bid_list['binance'] = []
            bid_list['binance'].append(float(data_list[i]['bidPrice']))
            # bid_list['binance'].append(float(data_list[i]['bids'][0][1]))
        elif i == 'wss://realtime.aax.com/marketdata/v2/':
            # print(data_list[i])
            ask_list['aax'] = []
            ask_list['aax'].append(float(data_list[i]['asks'][0][0]))
            bid_list['aax'] = []
            bid_list['aax'].append(float(data_list[i]['bids'][0][0]))
            # print(ask_list)
            # print(bid_list)
            # keyfunc = lambda x: x['price']
            # bids = [i for i in data_list[i]['result'] if i['side'] == 'Buy']
            # bids.sort(key=keyfunc)
            # asks = [i for i in data_list[i]['result'] if i['side'] == 'Sell']
            # asks.sort(key=keyfunc)
            # if asks:
            #     ask_list['bybit'] = []
            #     ask_list['bybit'].append(float(asks[-1]['price']))
            #     ask_list['bybit'].append(float(asks[-1]['size']))
            # if bids:
            #     bid_list['bybit'] = []
            #     bid_list['bybit'].append(float(bids[-1]['price']))
            #     bid_list['bybit'].append(float(bids[-1]['size']))

    if not long and not short:
        if bid_list['aax'][0] > ask_list['binance'][0]:
            short = bid_list['aax'][0]
            short_platform = 'aax'
            long = ask_list['binance'][0]
            long_platform = 'binance'
        else:
            long = ask_list['aax'][0]
            long_platform = 'aax'
            short = bid_list['binance'][0]
            short_platform = 'binance'

        print(long_platform, 'long', long, short_platform, 'short', short, 'time', datetime.datetime.now())

    fees = {'binance': 0.04, 'aax': 0.04}
    long_profit = bid_list[long_platform][0] - long
    short_profit = short - ask_list[short_platform][0]
    total_profit = long_profit + short_profit
    clear_profit = total_profit - ((long * (fees[long_platform] * 2) / 100) + (short * (fees[short_platform] * 2) / 100))
    # print(f'{long_platform} {ask_list[long_platform][0]}, long profit {long_profit}, {short_platform},  {bid_list[short_platform][0]}, short profit {short_profit}, total profit {total_profit}, clear profit {clear_profit}, Прибыль за сессию , time {datetime.datetime.now()}')
    # print(time.time() - start)
    # if total_profit > 80:
    if clear_profit > 0:
        max_profit += clear_profit
        print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, clear profit {clear_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
        long = 0
        short = 0