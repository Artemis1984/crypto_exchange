import requests
import time
import time
import asyncio
import aiohttp
import json
import datetime



# while True:
#     start = time.time()
#     # r = requests.get('https://api.aax.com/v2/market/orderbook?symbol=BTCUSDTFP&level=20').json()
#     r = requests.get('https://api.aax.com/v2/market/orderbook?symbol=BTCUSDTFP&level=20').json()
#     # r = requests.get('https://api.aax.com/v2/instruments').json()
#     # print(time.time() - start)
#     print(r)


links = [
         'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5',
         'https://api.aax.com/v2/market/orderbook?symbol=BTCUSDTFP&level=20'
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

        elif i == 'https://api.aax.com/v2/market/orderbook?symbol=BTCUSDTFP&level=20':
            try:
                ask_list['aax'] = []
                ask_list['aax'].append(float(data_list[i]['asks'][0][0]))
                ask_list['aax'].append(float(data_list[i]['asks'][0][1]))
            except:
                pass
            try:
                bid_list['aax'] = []
                bid_list['aax'].append(float(data_list[i]['bids'][0][0]))
                bid_list['aax'].append(float(data_list[i]['bids'][0][1]))
            except:
                pass

    if not long and not short:
        if bid_list['aax'][0] > ask_list['bitz'][0]:
            short = bid_list['aax'][0]
            short_platform = 'aax'
            long = ask_list['bitz'][0]
            long_platform = 'bitz'
        else:
            long = ask_list['aax'][0]
            long_platform = 'aax'
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


# import websocket

# socket = "wss://www.bitmex.com/realtime"
# socket = "wss://www.bitmex.com/realtime?subscribe=orderBookL2_25:LINKUSDT"
# socket = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"
# socket = "wss://realtime.aax.com/marketdata/v2/BTCUSDTFP@book_20"
#
#
# def on_open(ws):
#     print('Opened')
#
#
# def on_message(ws, messsage):
#     print(messsage)
#
#
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
# ws.run_forever()
# ws.close()
