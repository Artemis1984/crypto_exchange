import requests
from pprint import pprint
import json
import time
import asyncio
import aiohttp
import datetime


# start_time = time.time()

# response = requests.get('https://global.bittrex.com/v3/markets/')
# response = requests.get('https://global.bittrex.com/v3/markets/BTC-USDT/orderbook?depth=500')
# pprint(response.text)
# response = requests.get('ws://st.hitbtc.com/')
# response = requests.get('https://hitbtc.com/market-overview/all-trades')
# pprint(response.text)


# Bittrex API https://bittrex.github.io/api/v3#tag-Markets
# response = requests.get('https://api.bittrex.com/v3/markets/BTC-USDT/orderbook')
# pprint(json.loads(response.content))
# bid / ask

# Hitbtc API https://api.hitbtc.com/#order-book
# response = requests.get('https://api.hitbtc.com/api/2/public/orderbook')
# pprint(json.loads(response.content)['BTCTUSD'])
# bid / ask

# Kraken API https://www.kraken.com/features/api#get-order-book
# response = requests.get('https://api.kraken.com/0/public/Depth?pair=BTCUSDT')
# pprint(json.loads(response.content))
# bids / asks

# poloniex API https://docs.poloniex.com/#returnticker
# response = requests.get('https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=10')
# pprint(json.loads(response.content))
# bids / asks

# Kucoin API https://docs.kucoin.com/#base-url
# response = requests.get('https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol=BTC-USDT&limit=10')
# pprint(json.loads(response.content))
# bids / asks

# Huobi API https://huobiapi.github.io/docs/spot/v1/en/#get-market-depth
# response = requests.get('https://api.huobi.pro/market/depth?symbol=btcusdt&type=step1')
# pprint(json.loads(response.content))
# bids / asks

# Cex API https://cex.io/rest-api#orderbook
# response = requests.get('https://cex.io/api/order_book/BTC/USDT/?depth=5')
# pprint(json.loads(response.content))
# bids / asks

# Binance API https://binance-docs.github.io/apidocs/spot/en/#general-info
# response = requests.get('https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10')
# pprint(json.loads(response.content))
# bids / asks

# Exmo API https://documenter.getpostman.com/view/10287440/SzYXWKPi#78c08852-d5e7-4354-96a3-3bad5184bbfa
# response = requests.get('https://api.exmo.com/v1.1/order_book?pair=BTC_USDT&limit=5')
# pprint(json.loads(response.content))
# bid / ask

# Okex API https://www.okex.com/docs-v5/en/?python#rest-api-market-data-get-order-book
# response = requests.get('https://okex.com/api/v5/market/books?instId=BTC-USDT&sz=5')
# pprint(json.loads(response.content))
# bids / asks

# Bitfinex API https://docs.bitfinex.com/reference#rest-public-book
# response = requests.get('https://api-pub.bitfinex.com/v2/book/tBTCUSD/P0')
# pprint(json.loads(response.content))
# определяется по знаку объема по данной цене, то есть, if Объем > 0 bid else ask

# Ftx API got from browser
# response = requests.get('https://ftx.com/api/markets/BTC/USDT/trades?limit=25')
# response = json.loads(response.content)
# pprint(response)
# pprint(len([i for i in response['result'] if i['side'] == 'buy']))
# print('='*50)
# pprint(len([i for i in response['result'] if i['side'] == 'sell']))
# определяется по полю side, buy или sell

# Crypto API https://exchange-docs.crypto.com/#public-get-book
# response = requests.get('https://api.crypto.com/v2/public/get-book?instrument_name=BTC_USDT&depth=10')
# response = json.loads(response.content)
# pprint(response)
# float(data_list[i]['result']['data'][0]['bids'][0][0]
# float(data_list[i]['result']['data'][0]['asks'][0][0]


# Blockchain.com API https://api.blockchain.com/v3/#/unauthenticated


# print(time.time() - start_time)

fees = {'binance': 0.1, 'paritex': 0.15, 'ftx': 0.07, 'bybit': 0.075, 'bittrex': 0.2,
        'kraken': 0.26, 'poloniex': 0.125, 'kucoin': 0.1, 'huobi': 0.2, 'bitfinex': 0.2,
        'crypto.com': 0.16, 'blockchain.com': 0.4, 'bithumb': 0.1}

# 'https://trade.kucoin.com/_api/order-book/orderbook/level2?symbol=BTC-USDT&limit=10',
#  'https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10',
links = [
         # 'https://api.bittrex.com/v3/markets/BTC-USDT/orderbook',
         'https://api.kraken.com/0/public/Depth?pair=XBTUSDT',
         'https://api.huobi.pro/market/depth?symbol=btcusdt&type=step0',
         'https://api.kucoin.com/api/v1/market/orderbook/level2_20?symbol=BTC-USDT&limit=10',
         # 'https://poloniex.com/public?command=returnOrderBook&currencyPair=USDT_BTC&depth=10',
         'https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=10',
         'https://api-pub.bitfinex.com/v2/book/tBTCUST/P0',
         # 'https://ftx.com/api/markets/BTC/USDT/trades?limit=25',
         'https://api.crypto.com/v2/public/get-book?instrument_name=BTC_USDT&depth=10',
         # 'https://api.bybit.com/v2/public/orderBook/L2?symbol=BTCUSDT',
         # 'https://www.paritex.com/gateway/api-auth/api-ordermatch/api/v1/public/depth?symbol=BTCUSDT',
         # 'https://api.blockchain.com/v3/exchange/l2/BTC-USDT'
         'https://global-openapi.bithumb.pro/market/data/orderBook?symbol=BTC-USDT'
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


max_price = 0
max_profit = 0

if __name__ == '__main__':
    while True:
        start_time = time.time()
        asyncio.run(main())
        ask_list = dict()
        bid_list = dict()
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
            elif 'kraken' in i:
                try:
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['XBTUSDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['XBTUSDT']['asks'][0][1]))
                except:
                    print(data_list[i])
                    ask_list['kraken'] = []
                    ask_list['kraken'].append(float(data_list[i]['result']['BTC/USDT']['asks'][0][0]))
                    ask_list['kraken'].append(float(data_list[i]['result']['BTC/USDT']['asks'][0][1]))
                try:
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['XBTUSDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['XBTUSDT']['bids'][0][1]))
                except:
                    print(data_list[i])
                    bid_list['kraken'] = []
                    bid_list['kraken'].append(float(data_list[i]['result']['BTC/USDT']['bids'][0][0]))
                    bid_list['kraken'].append(float(data_list[i]['result']['BTC/USDT']['bids'][0][1]))

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
        # if temp_max_price > 300:
        #     buy_from = [[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]
        #     sell_to = [[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]
        #     price_diff = temp_max_price
        #     min_volume = min(buy_from[1][1], sell_to[1][1])
        #     Clear_profit = ((sell_to[1][0] * min_volume) - (buy_from[1][0] * min_volume)) - ((buy_from[1][0] * min_volume * fees[buy_from[0]] / 100) + (sell_to[1][0] * min_volume * fees[sell_to[0]] / 100))
        #     print('More then 300$', buy_from, sell_to, 'разница в цене', price_diff, '$', 'чистая прибыль', Clear_profit, 'time', datetime.datetime.now())
        #
        # if max_price < temp_max_price:
        #     with open('max_price_BTC.txt') as f:
        #         max_price_list = [f.read()]
        #     max_price = temp_max_price
        #     max_price_list.append(str([[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]) + ' - ' + str([[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]) + ' ' + str(max_price) + '$' + ' time - ' + str(datetime.datetime.now()) + '\n')
        #     with open('max_price_BTC.txt', 'w') as f:
        #         for k in max_price_list:
        #             f.write(k)
        # clear_profit = 0
        # if temp_max_price > 300:
        try:
            buy_from = [[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]
            sell_to = [[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]
            price_diff = temp_max_price
            min_volume = min(abs(buy_from[1][1]), abs(sell_to[1][1]))
            clear_profit = ((sell_to[1][0] * min_volume) - (buy_from[1][0] * min_volume)) - ((buy_from[1][0] * min_volume * fees[buy_from[0]] / 100) + (sell_to[1][0] * min_volume * fees[sell_to[0]] / 100))
            profit_percent = clear_profit / (buy_from[1][0] * min_volume) * 100
            # if clear_profit >= buy_from[1][0] * min_volume / 200:
            # if profit_percent >= 0.1:

            if clear_profit > 50:
                print(buy_from, sell_to, 'разница в цене', price_diff, '$', 'чистая прибыль', clear_profit, 'Прибыль %', profit_percent, 'time', datetime.datetime.now())
            if max_profit < clear_profit:
                with open('max_price_BTC.txt') as f:
                    max_price_list = [f.read()]
                max_profit = clear_profit
                max_price = temp_max_price
                # max_price_list.append(str([[i, ask_list[i]] for i in ask_list if ask_list[i][0] == min([i[0] for i in list(ask_list.values())])][0]) + ' - ' + str([[i, bid_list[i]] for i in bid_list if bid_list[i][0] == max([i[0] for i in list(bid_list.values())])][0]) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                max_price_list.append(str(buy_from) + ' - ' + str(sell_to) + ' ' + str(max_price) + '$ ' + 'Чистая прибыль ' + str(clear_profit) + '$ ' + 'Прибыль % ' + str(profit_percent) + ' time - ' + str(datetime.datetime.now()) + '\n')
                with open('max_price_BTC.txt', 'w') as f:
                    for k in max_price_list:
                        f.write(k)
        except:
            print(ask_list, bid_list)
            print(data_list)


        # print(time.time() - start_time)
