import requests
import datetime
import asyncio
import aiohttp
import json
import time

# BITZ API https://apidoc.bitz.ai/en/contract-market/Get-Order-Book.html
# print(requests.get('https://apiv2.bitz.com/Market/getContractOrderBook').json())
# print(requests.get('https://apiv2.bitz.com/Market/getContractCoin').json())
# while True:
#     print(requests.get('https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5').json())

# long = 0
# short = 0
# max_profit = 0
# # futures
# while True:
#     ask_list = {}
#     bid_list = {}
#     binance = requests.get('https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10').json()
#     bitz = requests.get('https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5').json()
#     # keyfunc = lambda x: x['price']
#     # bids = [i for i in bitz['result'] if i['side'] == 'Buy']
#     # bids.sort(key=keyfunc)
#     # asks = [i for i in bitz['result'] if i['side'] == 'Sell']
#     # asks.sort(key=keyfunc)
#     # if asks:
#     ask_list['bitz'] = []
#     ask_list['bitz'].append(float(bitz['data']['asks'][0]['price']))
#     ask_list['bitz'].append(float(bitz['data']['asks'][0]['amount']))
#     # if bids:
#     bid_list['bitz'] = []
#     bid_list['bitz'].append(float(bitz['data']['bids'][0]['price']))
#     bid_list['bitz'].append(float(bitz['data']['bids'][0]['amount']))
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
#
#     if not long and not short:
#         # long = ask_list['bitz'][0]
#         # short = bid_list['bitz'][0]
#         # short = bid_list['binance'][0]
#         # long = ask_list['binance'][0]
#         if bid_list['bitz'][0] > ask_list['binance'][0]:
#             short = bid_list['bitz'][0]
#             short_platform = 'bitz'
#             long = ask_list['binance'][0]
#             long_platform = 'binance'
#         else:
#             long = ask_list['bitz'][0]
#             long_platform = 'bitz'
#             short = bid_list['binance'][0]
#             short_platform = 'binance'
#
#         print(long_platform, 'long', long, short_platform, 'short', short)
#
#     # long_profit = bid_list['bitz'][0] - long
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
#     if total_profit > 15:
#         # if max_profit < total_profit:
#         #     max_profit = total_profit
#         max_profit += total_profit
#         print(f'{long_platform} long profit {long_profit}, {short_platform} short profit {short_profit}, total profit {total_profit}, Прибыль за сессию {max_profit}, time {datetime.datetime.now()}')
#         long = 0
#         short = 0


links = [
         'https://www.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=10',
         'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5'
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

        elif i == 'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5':
            ask_list['bitz'] = []
            ask_list['bitz'].append(float(data_list[i]['data']['asks'][0]['price']))
            ask_list['bitz'].append(float(data_list[i]['data']['asks'][0]['amount']))

            bid_list['bitz'] = []
            bid_list['bitz'].append(float(data_list[i]['data']['bids'][0]['price']))
            bid_list['bitz'].append(float(data_list[i]['data']['bids'][0]['amount']))

    if not long and not short:
        if bid_list['bitz'][0] > ask_list['binance'][0]:
            short = bid_list['bitz'][0]
            short_platform = 'bitz'
            long = ask_list['binance'][0]
            long_platform = 'binance'
        else:
            long = ask_list['bitz'][0]
            long_platform = 'bitz'
            short = bid_list['binance'][0]
            short_platform = 'binance'

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