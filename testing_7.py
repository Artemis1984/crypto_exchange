import requests
import time
import asyncio
import aiohttp
import json
import datetime


# while True:
#     start = time.time()
#     # r = requests.get('https://api.acdx.io/v1/contracts/BTC-PERP/book').json()
#     r = requests.get('https://api.basefex.com/depth@BTCUSDT/snapshot').json()
#     # ask = sorted([float(i) for i in r['asks']])[0]
#     # bid = sorted([float(i) for i in r['bids']])[-1]
#     asks = [[float(i), r['asks'][i]] for i in r['asks']]
#     bids = [[float(i), r['bids'][i]] for i in r['bids']]
#     asks.sort(key=lambda x: float(x[0]))
#     bids.sort(key=lambda x: float(x[0]))
#     print('ask', asks[0])
#     print('bid', bids[-1])
#     # print(time.time() - start)
#     # print('ask', r['bestPrices']['ask'])
#     # print('bid', r['bestPrices']['bid'])
#     print(r)
    # break

links = [
         'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5',
         'https://api.basefex.com/depth@BTCUSDT/snapshot'
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
        if i == 'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5':
            try:
                ask_list['bitz'] = []
                ask_list['bitz'].append(float(data_list[i]['data']['asks'][0]['price']))
                ask_list['bitz'].append(float(data_list[i]['data']['asks'][0]['amount']))
            except:
                pass
            try:
                bid_list['bitz'] = []
                bid_list['bitz'].append(float(data_list[i]['data']['bids'][0]['price']))
                bid_list['bitz'].append(float(data_list[i]['data']['bids'][0]['amount']))
            except:
                pass

        elif i == 'https://api.basefex.com/depth@BTCUSDT/snapshot':
            # asks = [[float(k), data_list[i]['asks'][k]] for k in data_list[i]['asks']]
            asks = [float(k) for k in data_list[i]['asks']]
            # bids = [[float(k), data_list[i]['bids'][k]] for k in data_list[i]['bids']]
            bids = [float(k) for k in data_list[i]['bids']]
            asks.sort(key=lambda x: x)
            bids.sort(key=lambda x: x)
            ask_list['basefex'] = []
            ask_list['basefex'].append(asks[0])
            bid_list['basefex'] = []
            bid_list['basefex'].append(bids[-1])
            # print(ask_list)
            # print(bid_list)
    if not long and not short:
        if bid_list['basefex'][0] > ask_list['bitz'][0]:
            short = bid_list['basefex'][0]
            short_platform = 'basefex'
            long = ask_list['bitz'][0]
            long_platform = 'bitz'
        else:
            long = ask_list['basefex'][0]
            long_platform = 'basefex'
            short = bid_list['bitz'][0]
            short_platform = 'bitz'

        print(long_platform, 'long', long, short_platform, 'short', short)

    long_profit = bid_list[long_platform][0] - long
    short_profit = short - ask_list[short_platform][0]
    total_profit = long_profit + short_profit

    # print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию , time {datetime.datetime.now()}')
    # print(time.time() - start)
    if total_profit > 80:
        max_profit += total_profit
        print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
        long = 0
        short = 0