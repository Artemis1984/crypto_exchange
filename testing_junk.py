import requests
import json
from pprint import pprint
import time
import datetime
import asyncio
import aiohttp


# links = [
#          'https://api.acdx.io/v1/contracts/BTC-PERP/book',
#          'https://apiv2.bitz.com/Market/getContractOrderBook?contractId=101&depth=5'
#          ]
#
# while True:
#     start = time.time()
#     r = requests.get(links[1]).json()
#     print(time.time() - start)


import websocket

# socket = "wss://www.bitmex.com/realtime"
# socket = "wss://www.bitmex.com/realtime?subscribe=orderBookL2_25:LINKUSDT"
# socket = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"
# socket = "wss://api.acdx.io/"
socket = "wss://api.acdx.io/"


def on_open(ws):
    print('Opened')
    ws.send(json.dumps(params.pop()))


def on_message(ws, messsage):
    print(messsage)


def on_pong(ws, messsage):
    print(messsage)


params = [{
            "type": "subscribe",
            "channels": ["level2"],
            "contract_codes": ["BTC-PERP"]
        }]
ws = websocket.WebSocketApp(socket, on_message=on_message, on_open=on_open)
ws.run_forever()
