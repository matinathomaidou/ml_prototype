# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 22:36:05 2016

@author: david
        Extended the work of Logicmn towards a batch job
@author: Matina
        Extended the work of Logicmn, David towards
        a web based micro-service
"""

# PYX (Python Exchange)
# Created by Logicmn
# Started 11/19/16

#                               -----------------------------------------
#                               | Real-time stock trading program using |
#                               |   a basic mean reversion algorithm    |
#                               -----------------------------------------

#-------------------------------------Dependencies and database link-------------------------------------------
import datetime
from yahoo_finance import Share

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, MetaData, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///new_db.db', echo=False) # Link the database to the SQLAlchemy engine
Session = sessionmaker(bind=engine)
Base = declarative_base()
metadata = MetaData()
session = Session()
#--------------------------------------------------------------------------------------------------------------

#-------------------------------------Creating tables for database--------------------------------------------
class Wallet(Base): # Create 'wallets' table
    __tablename__ = 'wallets'

    id = Column(Integer, Sequence('wallet_id_seq'), primary_key=True)
    name = Column(String)
    balance = Column(Integer)

    def __repr__(self):
        return "<Wallet(name='%s', balance='%s')>" % (self.name, self.balance)
        
class Symbols(Base): # Create 'synbols' table
    __tablename__ = 'shares'

    symbol = Column(String, Sequence('shares_id_seq'), primary_key=True)
    name = Column(String)
    exchange = Column(String)
    country = Column(String)
    category = Column(String)
    category_num = Column(String)

    def __repr__(self):
        return "<Symbols (shares='%s')>" % (self.symbol)       

class Transaction(Base): # Create 'transactions' table
    __tablename__ = 'transactions'

    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    stock = Column(String(50))
    symbol = Column(String(50))
    buy_or_sell = Column(String(50))
    price = Column(Integer())
    ema = Column(Integer())
    shares = Column(Integer())
    time = Column(String(50))

    def __repr__(self):
        return "<Transaction(stock='%s', symbol='%s', buy_or_sell='%s', price='%s', ema='%s', shares='%s', time='%s')>"\
               % (self.stock, self.symbol, self.buy_or_sell, self.price, self.ema, self.shares, self.time)
#--------------------------------------------------------------------------------------------------------------

#----------------------------------------Creating mean reversion algorithm-------------------------------------
class Strategy(object): # Create the algorithm PYX will use to trade with
    def __init__(self, equity):
        self.equity = equity

    def getEquity(self):
        return self.equity

    def calcEMA(self, close_price, prev_ema): # Calculate the exponential moving average
        multiplier = 2 / (50 + 1)
        ema = (close_price - prev_ema) * multiplier + prev_ema
        return ema

    def calcUpper(self, ema): # Calculate the upper Bollinger band
        upper_band = ema * (1 + .2)
        return upper_band

    def calcLower(self, ema): # Calculate the lower Bollinger band
        lower_band = ema * (1 - .2)
        return lower_band
#--------------------------------------------------------------------------------------------------------------

#------------------------------------------Buy/sell shares of a stock------------------------------------------
def enter_position(mean_reversion, apple): # Buy shares of a stock
    close_price, prev_ema, ema, lower_band, upper_band, purchase_query = calculations(mean_reversion, apple)
    new_funds=0
    if purchase_query != None:
        purchase = purchase_query[0]
    else:
        purchase = 'sell'
    if float(apple.get_price()) <= (lower_band) and purchase == 'sell': # Buy shares if the last purchase was a sell
        print('buy')
        new_transaction = Transaction(stock=apple.data_set['Name'], symbol=apple.data_set['symbol'], buy_or_sell='buy',
                                      price=apple.get_price(),
                                      ema=ema, shares='100', time=datetime.datetime.now())
        session.add(new_transaction)
        session.commit()
        print('Buy logic ', close_price, prev_ema, ema, lower_band, upper_band, purchase_query ) 
        new_funds = (float(apple.get_price()) * 100)
        balance = calc_wallet()
        new_bal = balance - new_funds # Subtract amount spent from the balance in wallet
        primary_wallet = Wallet(name='Primary Wallet', balance=new_bal) # Re-create wallet with new balance
        session.add(primary_wallet)
        session.commit()


def exit_position(mean_reversion, apple): 
    close_price, prev_ema, ema, lower_band, upper_band, purchase_query = calculations(mean_reversion, apple)
    new_funds=0
    if purchase_query != None:
        purchase = purchase_query[0]
    else:
        purchase = 'sell'
    if float(apple.get_price()) >= upper_band and purchase == 'buy': # Sell shares if the last purchase was a buy
        print('sell')
        new_transaction = Transaction(stock=apple.data_set['Name'], symbol=apple.data_set['symbol'], buy_or_sell='sell',
                                      price=(apple.get_price() * -1),
                                      ema=ema, shares='-100', time=datetime.datetime.now())
        new_funds = (float(apple.get_price()) * -100)                              
        session.add(new_transaction)
        session.commit()
        print('sell logic ', close_price, prev_ema, ema, lower_band, upper_band, purchase_query ) 
        balance = calc_wallet()
        new_bal = balance + new_funds # Add amount gained to the balance in wallet
        primary_wallet = Wallet(name='Primary Wallet', balance=new_bal) # Re-create wallet with new balance
        session.add(primary_wallet)
        session.commit()
 
#--------------------------------------------------------------------------------------------------------------

#-------------------------------------------------Calculations-------------------------------------------------
def calculations(mean_reversion, apple):
    close_price = float(apple.get_prev_close()) # Calculate yesterdays close price
    prev_ema = float(apple.get_50day_moving_avg()) # Calculate the previous EMA
    ema = mean_reversion.calcEMA(close_price, prev_ema) # Calculate the EMA
    lower_band, upper_band= float(mean_reversion.calcLower(ema)), float(mean_reversion.calcUpper(ema)) # Calculate the bands
    purchase_query = session.query(Transaction.buy_or_sell).order_by(Transaction.id.desc()).filter(Transaction.symbol == apple.data_set['symbol']).first() # Find out whether the latest purchase was a buy/sell
    return close_price, prev_ema, ema, lower_band, upper_band, purchase_query

def calc_wallet():
    #new_price = session.query(Transaction.price).order_by(Transaction.id.desc()).filter(Transaction.symbol == apple.data_set['symbol']).first() # Grab the bought price
    #new_shares = session.query(Transaction.shares).order_by(Transaction.id.desc()).filter(Transaction.symbol == apple.data_set['symbol']).first() # Grab how many shares were bought
    #new_funds = new_price[0] * new_shares[0] # Calculate the money spent
    balance = session.query(Wallet.balance).one() # Grab the current balance
    current_bal = session.query(Wallet).one()
    session.delete(current_bal) # Delete the wallet
    session.commit()
    return balance[0]
    
    
    
#--------------------------------------------------------------------------------------------------------------

#-------------------------------------------------Main function------------------------------------------------
def main():
    Base.metadata.create_all(engine)
    session.commit()
    b = session.query(Wallet.balance).first() # Check if there is already a wallet
    if b == None:
        primary_wallet = Wallet(name='Primary Wallet', balance=100000) # Create the wallet with a balance of $100,000
        session.add(primary_wallet)
        session.commit()
    sym = session.query(Symbols.symbol).order_by(Symbols.symbol).all()
    for symb in sym[0:750]:
# Which stock to monitor and invest in, make sure to change line 149 too
        try:
            apple = Share(symb[0]) 
            price = apple.get_price()
            price = float(price)
        except:
            continue
        try:
            print(symb[0], "being processed........")
            mean_reversion = Strategy(symb[0]) # Run the EMA, and Bollinger band calculations
            enter_position(mean_reversion, apple) # Buy stock if applicable
            exit_position(mean_reversion, apple) # Sell stock if applicable
            session.commit()
            print("Processed : ", symb[0])
        except:
            continue
    print("Done")
     
#--------------------------------------------------------------------------------------------------------------

#----Runs the program-----
if __name__ == "__main__":
    main()
