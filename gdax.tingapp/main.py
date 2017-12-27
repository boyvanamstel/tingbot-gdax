import tingbot
from tingbot import *
import gdax
import time

coins = ['BTC-EUR', 'ETH-EUR', 'LTC-EUR']

class TickerWebsocketClient(gdax.WebsocketClient):
    
    def __init__(self, products):
        super(TickerWebsocketClient, self).__init__(url="wss://ws-feed.gdax.com/", products=products, channels=['ticker'])

    def on_open(self):
        print("-- Hello! --")
        
        self.price = 0.0

    def on_message(self, msg):
        if 'price' in msg:
            self.price = float(msg['price'])
            
        time.sleep(1)
            
    def on_close(self):
        print("-- Goodbye! --")

class Ticker():
    
    def __init__(self, products):
        self.socket = None
        self.current_product = None
        
        self.products = products
        self.current_product_index = 0
        self.update_current_product()
        
        self.price = None
        self.previous_price = None

    def update_price(self):
        if self.socket != None:
            self.previous_price = self.price
            self.price = self.socket.price
        
    def update_current_product(self):
        if self.current_product_index < 0:
            self.current_product_index = len(self.products) - 1
        if self.current_product_index > len(self.products) - 1:
            self.current_product_index = 0
        
        self.price = 0.0
        
        self.current_product = self.products[self.current_product_index]
        
        if self.socket != None:
            self.socket.close()
            
        self.socket = TickerWebsocketClient([self.current_product])
        self.socket.start()
        
    def next_product(self):
        self.current_product_index += 1
        self.update_current_product()
        
    def previous_product(self):
        self.current_product_index -= 1
        self.update_current_product()

ticker = Ticker(coins)

def loop():
    if ticker.previous_price != ticker.price:

        screen.fill(color='white')
        
        screen.text(ticker.current_product, color='black', xy=(160,40), align='top', font_size=16)

        color = 'red' if ticker.previous_price > ticker.price else 'green'
        screen.text("EUR {:.2f}".format(ticker.price), color=color)

@every(seconds=0.5)
def update_ticker():
    ticker.update_price()

@midright_button.press
def increase_brightness():
    brightness = screen.brightness
    brightness += 10
    if brightness > 100:
        brightness = 100
        
    screen.brightness = brightness
    
@midleft_button.press
def decrease_brightness():
    brightness = screen.brightness
    brightness -= 10
    if brightness < 10:
        brightness = 10
        
    screen.brightness = brightness
    
@left_button.press
def previous_product():
    ticker.previous_product()
    
@right_button.press
def next_product():
    ticker.next_product()
    
tingbot.run(loop)
