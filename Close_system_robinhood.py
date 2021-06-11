import pandas as pd
import robin_stocks.robinhood as r
import pyotp
import time
from time import sleep
#https://github.com/jmfernandes/robin_stocks/blob/master/robin_stocks/robinhood/crypto.py


#------------------------Global variable---------------------------------

CLIENT_ID: str = "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS"
QR = str(input("Plase go to acount \n>>> security and Privacy >>> Two-Factor Authentication >>> manaul >>> get the code to fill here"))
username=str(input("Plase enter your username : "))
password=str(input("Plase enter your password : "))


frequency = int(input("Pleas enter frequency gap between the zone : "))
lot_side = float(input("Pleas enter lot side of the order : "))
print("Current OTP:", pyotp.TOTP(QR).now())
pd.set_option('display.max_columns', None)
login = r.login(username,password)
Open_order = pd.DataFrame(data = r.get_all_open_crypto_orders())
BTC = pd.DataFrame(data =r.get_crypto_positions(info=None))
Btc_avilable = float(max(BTC['quantity_available'].tolist()))
ask = float('%.2f' % float(r.get_crypto_quote("BTC")['ask_price']))
ask = int(float('%.2f' % (ask/10000))* 10000)-100
bid = float('%.2f' % float(r.get_crypto_quote("BTC")['bid_price']))
bid = int(float('%.2f' % (bid/10000))* 10000)

#------------------------------------------------------------------------

def check():
    Open = pd.DataFrame(data = Open_order[['side']])
    BUY = min(min(Open.values.tolist()))
    SELL = max(max(Open.values.tolist()))
    if BUY == "buy":
        low = Open_order[['price','side']].groupby(['side']).min()
        lower_zone = int('%.d' % (float(max(low.values.tolist()[0]))))
        high = Open_order[['price','side']].groupby(['side']).max()
        max_buy = int('%.d' % (float(max(high.values.tolist()[0]))))
        print("Your BTC lowest zone is", lower_zone)
        buying = max_buy
        selling = max_buy + 200
    else:
        buying = int(input("Plase enter the BTC price that you want to buy as lowest zone: "))
        r.order_buy_crypto_limit('BTC',lot_side,buying)
        selling = 0
    return(buying,selling)

def BUY(buying,frequency):
    while (buying <= bid-200):
        buying = buying + frequency
        r.order_buy_crypto_limit('BTC',lot_side,buying)
        print("Buy : ", buying)
        time.sleep(1)
    print("End of buying")
    
def Open_order_report():
    print("\n-------------Summery Open Order Report-------------\n\n",Open_order[['price','side','state']].sort_values(by=['price']))   
    print("BTC avilible : ",Btc_avilable)
    
def Sell(selling,frequency):
    if((Btc_avilable-0.0001)>= 0):
        while (selling >= ask+frequency):
            r.order_sell_crypto_limit('BTC',lot_side,selling)
            print("Sell : ", selling)
    print("End of selling")
        
def loop(frequency):
    for i in range (0,60):
        buying,selling = check()
        print(i+1 , "minutes")
        BUY(buying,frequency)
        Sell(selling,frequency)
        Open_order_report()
        time.sleep(60)

loop(frequency)
