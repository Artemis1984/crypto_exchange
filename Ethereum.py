import json
import time
import asyncio
import aiohttp
import datetime


# Upbit API https://global-docs.upbit.com/reference#order-book-list
# response = requests.get('https://sg-api.upbit.com/v1/orderbook', params={"markets": "USDT-BTC"})
# response = json.loads(response.content)
# pprint(response)


# response = requests.get('https://sg-api.upbit.com/v1/orderbook', params={"markets": "USDT-BTC"})
# response = json.loads(response.content)
# while True:
#     start = time.time()
    # response = requests.get('https://api.hitbtc.com/api/2/public/orderbook')
    # response = requests.get('https://poloniex.com/public?command=returnTicker')
    # response = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=10')

    # response = requests.get('https://ftx.com/api/markets/BTC/USDT/trades?limit=25')

    # response = requests.get('https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSDT')

    # testing ETH
    # response = requests.get('https://api.bittrex.com/v3/markets/ETH-USDT/orderbook')
    # response = requests.get('https://api.kraken.com/0/public/Depth?pair=ETHUSDT')
    # response = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_ETH&depth=10')
    # response = requests.get('https://trade.kucoin.com/_api/order-book/orderbook/level2?symbol=ETH-USDT&limit=10')
    # response = requests.get('https://api.huobi.pro/market/depth?symbol=ethusdt&type=step1')
    # response = requests.get('https://www.binance.com/api/v3/depth?symbol=ETHUSDT&limit=10')
    # response = requests.get('https://api-pub.bitfinex.com/v2/book/tETHUST/P0')
    # response = requests.get('https://ftx.com/api/markets/ETH/USDT/trades?limit=25')
    # response = requests.get('https://api.crypto.com/v2/public/get-book?instrument_name=ETH_USDT&depth=10')
    # response = requests.get('https://api.bybit.com/v2/public/orderBook/L2?symbol=ETHUSDT')
    # response = json.loads(response.content)
    # asks = [i['price'] for i in response['result'] if i['side'] == 'Sell']
    # bids = [i['price'] for i in response['result'] if i['side'] == 'Buy']
    # bids = [i['price'] for i in response['result'] if i['side'] == 'sell']
    # asks = [i['price'] for i in response['result'] if i['side'] == 'buy']
    # asks.sort()
    # bids.sort()
    # print(asks)
    # print(bids)
    # pprint(response)
    # print(time.time() - start)
    # break

# with open('max_price.txt') as f:
#     max_price = [f.read()]
    # max_price = f.read()
    # max_price = json.loads(max_price)

# print(max_price, type(max_price))
# max_price.append(max_price[-1])
# print(max_price, type(max_price))

links = [
         # 'https://api.bittrex.com/v3/markets/ETH-USDT/orderbook',
         'https://api.kraken.com/0/public/Depth?pair=ETHUSDT',
         # 'https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_ETH&depth=10',
         'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol=ETH-USDT&limit=10',
         'https://api.huobi.pro/market/depth?symbol=ethusdt&type=step0',
         'https://api.binance.com/api/v3/depth?symbol=ETHUSDT&limit=10',
         'https://api-pub.bitfinex.com/v2/book/tETHUST/P0',
         # 'https://ftx.com/api/markets/ETH/USDT/trades?limit=25',
         'https://api.crypto.com/v2/public/get-book?instrument_name=ETH_USDT&depth=10',
         # 'https://api.bybit.com/v2/public/orderBook/L2?symbol=ETHUSDT',
         # 'https://www.paritex.com/gateway/api-auth/api-ordermatch/api/v1/public/depth?symbol=ETHUSDT',
         # 'https://api.blockchain.com/v3/exchange/l2/ETH-USDT'
         'https://global-openapi.bithumb.pro/market/data/orderBook?symbol=ETH-USDT'
         ]

fees = {'binance': 0.1, 'paritex': 0.15, 'ftx': 0.07, 'bybit': 0.075, 'bittrex': 0.2,
        'kraken': 0.26, 'poloniex': 0.125, 'kucoin': 0.1, 'huobi': 0.2, 'bitfinex': 0.2,
        'crypto.com': 0.16, 'blockchain.com': 0.4, 'bithumb': 0.1}

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


max_price = 0
max_profit = 0

if __name__ == '__main__':
    while True:
        start_time = time.time()
        asyncio.run(main())
        ask_list = dict()
        bid_list = dict()
        # pprint(data_list)
        for i in data_list:
            if 'bittrex' in i:
                try:
                    ask_list['bittrex'] = []
                    ask_list['bittrex'].append(float(data_list[i]['ask'][0]['rate']))
                    ask_list['bittrex'].append(float(data_list[i]['ask'][0]['quantity']))
                except:
                    pass
                try:
                    bid_list['bittrex'] = []
                    bid_list['bittrex'].append(float(data_list[i]['bid'][0]['rate']))
                    bid_list['bittrex'].append(float(data_list[i]['bid'][0]['quantity']))
                except:
                    pass
                # print('ask', data_list[i]['ask'][0], 'bid', data_list[i]['bid'][0])
                # print(ask_list['bittrex'], bid_list['bittrex'])
            elif 'kraken' in i:
                try:
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['ETHUSDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['ETHUSDT']['asks'][0][1]))
                except:
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['ETH/USDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['ETH/USDT']['asks'][0][1]))
                try:
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['ETHUSDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['ETHUSDT']['bids'][0][1]))
                except:
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['ETH/USDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['ETH/USDT']['bids'][0][1]))
                # print('ask', data_list[i]['result']['XBTUSDT']['asks'][0], 'bid', data_list[i]['result']['XBTUSDT']['bids'][0])
            elif 'poloniex' in i:
                try:
                    ask_list['poloniex'] = []
                    ask_list['poloniex'].append(float(data_list[i]['asks'][0][0]))
                    ask_list['poloniex'].append(float(data_list[i]['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['poloniex'] = []
                    bid_list['poloniex'].append(float(data_list[i]['bids'][0][0]))
                    bid_list['poloniex'].append(float(data_list[i]['bids'][0][1]))
                except:
                    pass
                # print('ask', data_list[i]['asks'][0], 'bid', data_list[i]['bids'][0])
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
                # print('ask', data_list[i]['data']['asks'][0], 'bid', data_list[i]['data']['bids'][0])
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
                # print('ask', data_list[i]['tick']['asks'][0], 'bid', data_list[i]['tick']['bids'][0])
            elif 'binance' in i:
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
            elif 'ftx' in i:
                if 'result' in data_list[i]:
                    keyfunc = lambda x: x['price']
                    asks = [i for i in data_list[i]['result'] if i['side'] == 'buy']
                    asks.sort(key=keyfunc)
                    bids = [i for i in data_list[i]['result'] if i['side'] == 'sell']
                    bids.sort(key=keyfunc)
                    if asks:
                        ask_list['ftx'] = []
                        ask_list['ftx'].append(float(asks[-1]['price']))
                        ask_list['ftx'].append(float(asks[-1]['size']))
                    if bids:
                        bid_list['ftx'] = []
                        bid_list['ftx'].append(float(bids[-1]['price']))
                        bid_list['ftx'].append(float(bids[-1]['size']))
                        # print('FTX', 'bids', bids[-1], '\n', 'asks', asks[-1])
            elif 'crypto.com' in i:
                try:
                    ask_list['crypto.com'] = []
                    ask_list['crypto.com'].append(float(data_list[i]['result']['data'][0]['asks'][0][0]))
                    ask_list['crypto.com'].append(float(data_list[i]['result']['data'][0]['asks'][0][1]))
                except:
                    pass
                try:
                    bid_list['crypto.com'] = []
                    bid_list['crypto.com'].append(float(data_list[i]['result']['data'][0]['bids'][0][0]))
                    bid_list['crypto.com'].append(float(data_list[i]['result']['data'][0]['bids'][0][1]))
                except:
                    pass
                # print('Crypto', 'ask', float(data_list[i]['result']['data'][0]['asks'][0][0]), 'bid', float(data_list[i]['result']['data'][0]['bids'][0][0]))
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
                # print(ask_list, bid_list)
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
            elif 'blockchain.com' in i:
                try:
                    ask_list['blockchain.com'] = []
                    ask_list['blockchain.com'].append(float(data_list[i]['asks'][0]['px']))
                    ask_list['blockchain.com'].append(float(data_list[i]['asks'][0]['qty']))
                except:
                    pass
                try:
                    bid_list['blockchain.com'] = []
                    bid_list['blockchain.com'].append(float(data_list[i]['bids'][0]['px']))
                    bid_list['blockchain.com'].append(float(data_list[i]['bids'][0]['qty']))
                except:
                    pass
            elif 'bithumb' in i:
                try:
                    ask_list['bithumb'] = []
                    ask_list['bithumb'].append(float(data_list[i]['info']['s'][0][0]))
                    ask_list['bithumb'].append(float(data_list[i]['info']['s'][0][1]))
                except:
                    pass
                try:
                    bid_list['bithumb'] = []
                    bid_list['bithumb'].append(float(data_list[i]['info']['b'][0][0]))
                    bid_list['bithumb'].append(float(data_list[i]['info']['b'][0][1]))
                except:
                    pass

        temp_max_price = 0
        try:
            temp_max_price = max([i[0] for i in list(bid_list.values())]) - min([i[0] for i in list(ask_list.values())])
        except:
            pass
        # if temp_max_price > 10:
        #     buy_from = [[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]
        #     sell_to = [[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]
        #     price_diff = temp_max_price
        #     min_volume = min(buy_from[1][1], sell_to[1][1])
        #     Clear_profit = ((sell_to[1][0] * min_volume) - (buy_from[1][0] * min_volume)) - ((buy_from[1][0] * min_volume * fees[buy_from[0]] / 100) + (sell_to[1][0] * min_volume * fees[sell_to[0]] / 100))
        #     print('More then 10$', buy_from, sell_to, 'разница в цене', price_diff, '$', 'чистая прибыль', Clear_profit, 'time', datetime.datetime.now())
        #
        # if max_price < temp_max_price:
        #     with open('max_price_ETH.txt') as f:
        #         max_price_list = [f.read()]
        #     max_price = temp_max_price
        #     max_price_list.append(str([[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]) + ' - ' + str([[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]) + ' ' + str(max_price) + '$' + ' time - ' + str(datetime.datetime.now()) + '\n')
        #     with open('max_price_ETH.txt', 'w') as f:
        #         for k in max_price_list:
        #             f.write(k)

        # clear_profit = 0
        # if temp_max_price > 10:
        try:
            buy_from = [[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]
            sell_to = [[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]
            price_diff = temp_max_price
            min_volume = min(abs(buy_from[1][1]), abs(sell_to[1][1]))
            clear_profit = ((sell_to[1][0] * min_volume) - (buy_from[1][0] * min_volume)) - ((buy_from[1][0] * min_volume * fees[buy_from[0]] / 100) + (sell_to[1][0] * min_volume * fees[sell_to[0]] / 100))
            profit_percent = clear_profit / (buy_from[1][0] * min_volume) * 100
            # if clear_profit >= buy_from[1][0] * min_volume / 200:
            # if profit_percent >= 0.1:
            if clear_profit > 10:
                print(buy_from, sell_to, 'разница в цене', price_diff, '$', 'чистая прибыль', clear_profit, 'Прибыль %', profit_percent, 'time', datetime.datetime.now())
            if max_profit < clear_profit:
                with open('max_price_ETH.txt') as f:
                    max_price_list = [f.read()]
                max_profit = clear_profit
                max_price = temp_max_price
                # max_price_list.append(str([[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]) + ' - ' + str([[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                max_price_list.append(str(buy_from) + ' - ' + str(sell_to) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                with open('max_price_ETH.txt', 'w') as f:
                    for k in max_price_list:
                        f.write(k)

        except:
            print('exception')
            print(ask_list, bid_list)
            print(data_list)
        # print(time.time() - start_time)
