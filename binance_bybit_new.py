import requests
import json
from pprint import pprint
import time
import datetime
import asyncio
import aiohttp


links = [
         'https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT',
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
total_profit = 0
# take profit, stop loss
tPsL = {'binance': {'stop_loss': -1000000, 'take_profit': 1000}, 'bybit': {'stop_loss': -1000000, 'take_profit': 1000}}
trigger = None
short_profit = None
long_profit = None
charge = True


while True:
    start = time.time()
    asyncio.run(main())
    ask_list = dict()
    bid_list = dict()
    for i in data_list:
        if i == 'https://www.binance.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT':
            ask_list['binance'] = []
            ask_list['binance'].append(float(data_list[i]['askPrice']))
            # ask_list['binance'].append(float(data_list[i]['asks'][0][1]))

            bid_list['binance'] = []
            bid_list['binance'].append(float(data_list[i]['bidPrice']))
            # bid_list['binance'].append(float(data_list[i]['bids'][0][1]))
        elif i == 'https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT':
            ask_list['bybit'] = []
            ask_list['bybit'].append(float(data_list[i]['result'][0]['ask_price']))
            bid_list['bybit'] = []
            bid_list['bybit'].append(float(data_list[i]['result'][0]['bid_price']))
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
        # print('прибыль за сессию', total_profit)
        if bid_list['bybit'][0] > ask_list['binance'][0]:
            short = bid_list['bybit'][0] * 10
            short_platform = 'bybit'
            long = ask_list['binance'][0] * 10
            long_platform = 'binance'
        else:
            long = ask_list['bybit'][0] * 10
            long_platform = 'bybit'
            short = bid_list['binance'][0] * 10
            short_platform = 'binance'

        print('long', long_platform, long, 'short', short_platform, short, 'time', datetime.datetime.now())
    fees = {'binance': 0.02, 'bybit': 0.05}
#   Начинаем с начала

    if charge:
        long_profit = (bid_list[long_platform][0] * 10) - long - (long * (fees[long_platform] * 2) / 100)
        short_profit = short - (ask_list[short_platform][0] * 10) - (short * (fees[short_platform] * 2) / 100)
        if long_profit > tPsL[long_platform]['take_profit']:
            total_profit += long_profit
            print('total profit', total_profit, long_platform, 'фиксирована прибыль')
            print('long profit', long_platform, long_profit, 'short profit', short_platform, short_profit, 'total profit', total_profit, 'time', datetime.datetime.now())
            print('trigger price', bid_list[short_platform][0])
            trigger = {'side': 'short', 'platform': short_platform, 'price': bid_list[short_platform][0]}
            tPsL[long_platform]['stop_loss'] = total_profit * 5 / 100
            tPsL[long_platform]['take_profit'] = total_profit * 5 / 100
            charge = False
        elif long_profit <= tPsL[long_platform]['stop_loss']:
            total_profit += tPsL[long_platform]['stop_loss'] - (long * (fees[long_platform] * 2) / 100)
            charge = False
        elif short_profit > tPsL[short_platform]['take_profit']:
            total_profit += short_profit
            print('total profit', total_profit, short_platform, 'фиксирована прибыль')
            print('long profit', long_platform, long_profit, 'short profit', short_platform, short_profit, 'total profit', total_profit, 'time', datetime.datetime.now())
            print('trigger price', ask_list[long_platform][0])
            trigger = {'side': 'long', 'platform': long_platform, 'price': ask_list[long_platform][0]}
            tPsL[short_platform]['stop_loss'] = total_profit * 5 / 100
            tPsL[short_platform]['take_profit'] = total_profit * 5 / 100
            charge = False
        elif short_profit <= tPsL[short_platform]['stop_loss']:
            total_profit += tPsL[short_platform]['stop_loss'] - (short * (fees[short_platform] * 2) / 100)
            charge = False
    else:
        if trigger['side'] == 'short':
            if ask_list[trigger['platform']][0] >= trigger['price']:
                long = trigger['price'] * 10
                charge = True
            short_profit = short - (ask_list[short_platform][0] * 10 ) - (short * (fees[short_platform] * 2) / 100)
            if total_profit + short_profit >= 500:
                print('Прибыль', total_profit + short_profit, 'ордер закрыт','total profit', total_profit, 'short profit', short_platform, short_profit, 'time', datetime.datetime.now())
                long, short, total_profit = None, None, 0
                time.sleep(100)
                # break
        else:
            if bid_list[trigger['platform']][0] <= trigger['price']:
                short = trigger['price'] * 10
                charge = True
            long_profit = (bid_list[long_platform][0] * 10) - long - (long * (fees[long_platform] * 2) / 100)
            if total_profit + long_profit >= 500:
                print('Прибыль', total_profit + short_profit, 'short was closed, long is open', long_platform, long_profit, 'time', datetime.datetime.now())
                long, short, total_profit = None, None, 0
                # break

    # print('long profit', long_platform, long_profit, 'short profit', short_platform, short_profit, 'total profit', total_profit, 'time', datetime.datetime.now())





















