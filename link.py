import json
import time
import asyncio
import aiohttp
import datetime


fees = {'binance': 0.1, 'paritex': 0.15, 'ftx': 0.07, 'bybit': 0.075, 'bittrex': 0.2,
        'kraken': 0.26, 'poloniex': 0.125, 'kucoin': 0.1, 'huobi': 0.2, 'bitfinex': 0.2,
        'crypto.com': 0.16, 'blockchain.com': 0.4}

links = [
         'https://api.binance.com/api/v3/depth?symbol=LINKUSDT&limit=10',
         'https://api-pub.bitfinex.com/v2/book/tLINK:UST/P0',
         'https://api.huobi.pro/market/depth?symbol=linkusdt&type=step0',
         # 'https://api.bybit.com/v2/public/orderBook/L2?symbol=LINKUSDT',
         # 'https://www.bitmex.com/api/v1/orderBook/L2?symbol=LINKUSDT&depth=25'
         'https://api.kraken.com/0/public/Depth?pair=LINKUSDT',
         'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol=LINK-USDT&limit=10',
         'https://api.crypto.com/v2/public/get-book?instrument_name=LINK_USDT&depth=10'
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

# 9689611311

max_price = 0
max_profit = 0

if __name__ == '__main__':
    while True:
        start_time = time.time()
        asyncio.run(main())
        ask_list = dict()
        bid_list = dict()
        for i in data_list:
            if 'binance' in i:
                try:
                    ask_list['binance'] = []
                    ask_list['binance'].append(float(data_list[i]['asks'][0][0]))
                    ask_list['binance'].append(float(data_list[i]['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['binance'] = []
                    bid_list['binance'].append(float(data_list[i]['bids'][0][0]))
                    bid_list['binance'].append(float(data_list[i]['bids'][0][1]))
                except:
                    pass
                # print('ask', data_list[i]['asks'][0], 'bid', data_list[i]['bids'][0])
            elif 'bitfinex' in i:
                for k in data_list[i]:
                    if k[2] < 0:
                        ask_list['bitfinex'] = []
                        ask_list['bitfinex'].append(float(data_list[i][data_list[i].index(k)][0]))
                        ask_list['bitfinex'].append(float(data_list[i][data_list[i].index(k)][2]))
                        bid_list['bitfinex'] = []
                        bid_list['bitfinex'].append(float(data_list[i][0][0]))
                        bid_list['bitfinex'].append(float(data_list[i][0][2]))
                        # print('ask', data_list[i][data_list[i].index(k)], 'bid', data_list[i][0])
                        break
                # print(ask_list, bid_list)
            elif 'bybit' in i:
                if 'result' in data_list[i]:
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
            elif 'bitmex' in data_list[i]:
                if 'result' in data_list[i]:
                    keyfunc = lambda x: x['price']
                    bids = [i for i in data_list[i]['result'] if i['side'] == 'Buy']
                    # bids.sort(key=keyfunc)
                    asks = [i for i in data_list[i]['result'] if i['side'] == 'Sell']
                    # asks.sort(key=keyfunc)
                    if asks:
                        ask_list['bitmex'] = []
                        ask_list['bitmex'].append(float(asks[0]['price']))
                        ask_list['bitmex'].append(float(asks[0]['size']))
                    if bids:
                        bid_list['bitmex'] = []
                        bid_list['bitmex'].append(float(bids[0]['price']))
                        bid_list['bitmex'].append(float(bids[0]['size']))
            elif 'kraken' in i:
                try:
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['LINKUSDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['LINKUSDT']['asks'][0][1]))
                except:
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['LINK/USDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['LINK/USDT']['asks'][0][1]))
                try:
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['LINKUSDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['LINKUSDT']['bids'][0][1]))
                except:
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['LINK/USDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['LINK/USDT']['bids'][0][1]))
            elif 'huobi' in i:
                try:
                    ask_list['huobi'] = []
                    ask_list['huobi'].append(float(data_list[i]['tick']['asks'][0][0]))
                    ask_list['huobi'].append(float(data_list[i]['tick']['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['huobi'] = []
                    bid_list['huobi'].append(float(data_list[i]['tick']['bids'][0][0]))
                    bid_list['huobi'].append(float(data_list[i]['tick']['bids'][0][1]))
                except:
                    pass
            elif 'kucoin' in i:
                try:
                    ask_list['kucoin'] = []
                    ask_list['kucoin'].append(float(data_list[i]['data']['asks'][0][0]))
                    ask_list['kucoin'].append(float(data_list[i]['data']['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['kucoin'] = []
                    bid_list['kucoin'].append(float(data_list[i]['data']['bids'][0][0]))
                    bid_list['kucoin'].append(float(data_list[i]['data']['bids'][0][1]))
                except:
                    pass
            elif 'paritex' in i:
                try:
                    ask_list['paritex'] = []
                    ask_list['paritex'].append(float(data_list[i]['data']['asks'][0][0]))
                    ask_list['paritex'].append(float(data_list[i]['data']['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['paritex'] = []
                    bid_list['paritex'].append(float(data_list[i]['data']['bids'][0][0]))
                    bid_list['paritex'].append(float(data_list[i]['data']['bids'][0][1]))
                except:
                    pass

        temp_max_price = 0
        try:
            temp_max_price = max([i[0] for i in list(bid_list.values())]) - min([i[0] for i in list(ask_list.values())])
        except:
            pass

        # clear_profit = 0
        # if temp_max_price > 0.2:
        # print(ask_list, bid_list)
        try:
            buy_from = [[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]
            sell_to = [[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]
            price_diff = temp_max_price
            min_volume = min(abs(buy_from[1][1]), abs(sell_to[1][1]))
            clear_profit = ((sell_to[1][0] * min_volume) - (buy_from[1][0] * min_volume)) - ((buy_from[1][0] * min_volume * fees[buy_from[0]] / 100) + (sell_to[1][0] * min_volume * fees[sell_to[0]] / 100))
            profit_percent = clear_profit / (buy_from[1][0] * min_volume) * 100
            # if clear_profit >= buy_from[1][0] * min_volume / 200:
            # if profit_percent >= 0.1:
            if clear_profit > 2:
                print(buy_from, sell_to, 'разница в цене', price_diff, '$', 'чистая прибыль', clear_profit, 'Прибыль %', profit_percent, 'time', datetime.datetime.now())
            if max_profit < clear_profit:
                with open('max_price_LINK.txt') as f:
                    max_price_list = [f.read()]
                max_profit = clear_profit
                max_price = temp_max_price
                # max_price_list.append(str([[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]) + ' - ' + str([[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                max_price_list.append(str(buy_from) + ' - ' + str(sell_to) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                with open('max_price_LINK.txt', 'w') as f:
                    for k in max_price_list:
                        f.write(k)
        except:
            print('exception')
            print(ask_list, bid_list)
            print(data_list)
        # print(time.time() - start_time)

