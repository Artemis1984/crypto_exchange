import requests
import json
from pprint import pprint
import time
import datetime
import asyncio
import aiohttp

# while True:
#     # start = time.time()
#     # r = requests.get('https://futures-api.poloniex.com/api/v1/level2/depth?symbol=BTCUSDTPERP&depth=depth5').json()
#     r = requests.get('https://futures-rest.poloniex.com/futures-market/v1/level2/snapshot?symbol=BTCUSDTPERP').json()
#     print(r)
    # print(time.time() - start)

# /contract/instrument:{symbol}

links = [
         'https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10',
         'https://futures-rest.poloniex.com/futures-market/v1/level2/snapshot?symbol=BTCUSDTPERP'
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

        elif i == 'https://futures-rest.poloniex.com/futures-market/v1/level2/snapshot?symbol=BTCUSDTPERP':
            try:
                ask_list['poloniex'] = []
                ask_list['poloniex'].append(float(data_list[i]['data']['asks'][0][0]))
                ask_list['poloniex'].append(float(data_list[i]['data']['asks'][0][1]))
            except:
                pass
            try:
                bid_list['poloniex'] = []
                bid_list['poloniex'].append(float(data_list[i]['data']['bids'][0][0]))
                bid_list['poloniex'].append(float(data_list[i]['data']['bids'][0][1]))
            except:
                pass

    if not long and not short:
        if bid_list['poloniex'][0] > ask_list['binance'][0]:
            short = bid_list['poloniex'][0]
            short_platform = 'poloniex'
            long = ask_list['binance'][0]
            long_platform = 'binance'
        else:
            long = ask_list['poloniex'][0]
            long_platform = 'poloniex'
            short = bid_list['binance'][0]
            short_platform = 'binance'

        print(long_platform, 'long', long, short_platform, 'short', short, 'time', datetime.datetime.now())

    fees = {'binance': 0.04, 'poloniex': 0.075}
    long_profit = bid_list[long_platform][0] - long
    short_profit = short - ask_list[short_platform][0]
    total_profit = long_profit + short_profit
    clear_profit = total_profit - ((long * (fees[long_platform] * 2) / 100) + (short * (fees[short_platform] * 2) / 100))

    # print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию , time {datetime.datetime.now()}')
    # print(time.time() - start)
    if clear_profit > 0:
        max_profit += clear_profit
        # print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
        print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, clear profit {clear_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
        long = 0
        short = 0
