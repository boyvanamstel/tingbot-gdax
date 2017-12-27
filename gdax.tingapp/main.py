import tingbot
from tingbot import *
import gdax
import time

class TickerWebsocketClient(gdax.WebsocketClient):
    
    def on_open(self):
        self.price = 0.0
        self.url = "wss://ws-feed.gdax.com/"
        self.channels = ["ticker"]
        self.products = ["BTC-EUR"]

    def on_message(self, msg):
        if 'price' in msg and 'side' in msg:
            if msg['side'] == "buy":
                self.price = float(msg['price'])
        time.sleep(1)
            
    def on_close(self):
        print("-- Goodbye! --")

tickerSocket = TickerWebsocketClient()
tickerSocket.start()

class Ticker():
    
    def __init__(self):
        self.price = 0.0
        self.previous_price = 0.0
        
    def updatePrice(self, value):
        self.previous_price = self.price
        self.price = value
        
ticker = Ticker()

def loop():
    if ticker.previous_price != ticker.price:

        screen.fill(color='white')

        color = 'red' if ticker.previous_price > ticker.price else 'green'
        screen.text("EUR {:.2f}".format(ticker.price), color=color)

@every(seconds=1)
def updateTicker():
    ticker.updatePrice(tickerSocket.price)

tingbot.run(loop)
