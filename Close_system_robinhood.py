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


print("Current OTP:", pyotp.TOTP(QR).now())
pd.set_option('display.max_columns', None)
login = r.login(username,password)
BTC = pd.DataFrame(data =r.get_crypto_positions(info=None))
Btc_avilable = float(max(BTC['quantity_available'].tolist()))
ask = float('%.2f' % float(r.get_crypto_quote("BTC")['ask_price']))
ask = int(float('%.2f' % (ask/10000))* 10000)-100
bid = float('%.2f' % float(r.get_crypto_quote("BTC")['bid_price']))
bid = int(float('%.2f' % (bid/10000))* 10000)
BTC = pd.DataFrame(data =r.get_crypto_positions(info=None))
Btc_avilable = float(max(BTC['quantity_available'].tolist()))
    
#------------------------------------------------------------------------
def parameter(Open_order):
    low = Open_order[['price','side']].groupby(['side']).min()
    lower_zone = int('%.d' % (float(min(low.values.tolist()[0]))))
    high = Open_order[['price','side']].groupby(['side']).max()
    print("Your BTC lowest zone is", lower_zone)
    min_sell = int('%.d' % (float(min(low.values.tolist()[1]))))
    return (low,lower_zone,high,min_sell)

def check(Start_buy):
    Open_order = pd.DataFrame(data = r.get_all_open_crypto_orders())
    Open = pd.DataFrame(data = Open_order[['side']])
    BUY = min(min(Open.values.tolist()))
    SELL = max(max(Open.values.tolist()))
    if BUY == "buy":
        low,lower_zone,high,min_sell = parameter(Open_order)
        max_buy = int('%.d' % (float(max(high.values.tolist()[0]))))
        buying = max_buy
        if SELL == "sell":
            selling = min_sell
        else:
            selling = buy_max + 200
        return(buying,selling)
    else:
        print("----------")
        time.sleep(10)
        buying = Start_buy
        if (Btc_avilable-0.00001)>= 0:
            if SELL == "sell":
                low = Open_order[['price','side']].groupby(['side']).min()
                selling = int('%.d' % (float(min(low.values.tolist()[1]))))
            else:
                selling = int(input("There are some BTC in the port. How much do you want to sell : "))
        else:
            selling = 99999999
        return(buying,selling)

def BUY(buying,frequency,Start_buy,lot_side):
    while (buying <= bid-200):
        buying = buying + frequency
        if buying <= Start_buy:
            print("Your buy orders are matched")
            time.sleep(1)
        else:
            r.order_buy_crypto_limit('BTC',lot_side,buying)
            print("Buy : ", buying)
            time.sleep(1)
    print("End of buying")
    
def Open_order_report():
    Open_order = pd.DataFrame(data = r.get_all_open_crypto_orders())
    print("\n-------------Summery Open Order Report-------------\n\n",Open_order[['price','side','state']].sort_values(by=['price']))   
    print("BTC avilible : ",Btc_avilable)
    return()
    
def Sell(selling,frequency,Btc_avilable,lot_side):
    while((Btc_avilable-0.00001)>= 0):
        if (selling >= ask+100):
            selling = selling - frequency
            #r.order_sell_crypto_limit('BTC',lot_side,selling)
            print("Sell : ", selling)
        BTC = pd.DataFrame(data =r.get_crypto_positions(info=None))
        Btc_avilable = float(max(BTC['quantity_available'].tolist()))
    print("End of selling")
        
def loop(Btc_avilable):
    Start_buy = int(input("Plase enter the BTC price that you want to buy as lowest zone: "))
    frequency = int(input("Pleas enter frequency gap between the zone : "))
    lot_side = float(input("Pleas enter lot side of the order : "))
    for i in range (0,60):
        buying,selling = check(Start_buy)
        print(i+1 , "minutes")
        BUY(buying,frequency,Start_buy,lot_side)
        Sell(selling,frequency,Btc_avilable,lot_side)
        Open_order_report()
        time.sleep(60)

loop(Btc_avilable)
