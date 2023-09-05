# LOAD LIBRARIES
import math
import mysql.connector
#import datetime
import yfinance as yf
from yahoofinancials import YahooFinancials
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

######################################################################
data = pd.DataFrame() # INIT EMPTY DATAFRAME OBJECT TO CONCAT FINAL OUTPUT
symbol_list = "" # CREATE EMPTY STRING VAR
fundamental_valuations = pd.DataFrame() # CREATE EMPTY DATAFRAME

######################################################################
# LOAD LIST OF STOCKS TO INSERT INTO THE DATABASE
stock_list = pd.read_csv("Data/Symbols-TEST.csv") # TESTING DATA FILE

#stock_list = pd.read_csv("Data/Symbols-Communications-Services.csv")
#stock_list = pd.read_csv("Data/Symbols-Consumer-Discretionary.csv")
#stock_list = pd.read_csv("Data/Symbols-Consumer-Staples.csv")
#stock_list = pd.read_csv("Data/Symbols-Energy.csv")
#stock_list = pd.read_csv("Data/Symbols-Financials.csv")
#stock_list = pd.read_csv("Data/Symbols-Health-Care.csv")
#stock_list = pd.read_csv("Data/Symbols-Industrials.csv")
#stock_list = pd.read_csv("Data/Symbols-Information-Technology.csv")
#stock_list = pd.read_csv("Data/Symbols-Materials.csv")
#stock_list = pd.read_csv("Data/Symbols-Real-Estate.csv")
#stock_list = pd.read_csv("Data/Symbols-Utilities.csv")

######################################################################
# CREATE CONNECTION TO THE DATABASE
cnx = mysql.connector.connect(user='vsc', password='blaster123',
                              host='127.0.0.1',
                              database='stockdata')

# CREATE A CURSORS TO THE DATABASE
cursor = cnx.cursor(buffered=True) 
mycursor = cnx.cursor()

#dhr = yf.Ticker('DHR')
#info = dhr.info
#info.keys()

for x in stock_list['Symbol']:
    # GET FUNDAMENTALS HISTORY
    #yahoo_financials = YahooFinancials(x)
    financials = yf.Ticker(x)
    fundamental_val = pd.DataFrame(financials.info)
    #fundamental_valuations['date'] = pd.to_datetime(fundamental_valuations['date']/1000, unit="s")
    #fundamental_valuations['date'] = pd.to_datetime(fundamental_valuations['date'], unit="s")
    f_filename = x + '-Fundamentals.csv'
    fundamental_val.to_csv('Data/Fundamentals/' + f_filename)

    # GET PRICE HISTORY
    price_val = yf.download(x) # GET ALL PRICE DATA FOR SYMBOL FROM YFINANCE
    p_filename = x + '-Price-History.csv'
    price_val.to_csv('Data/Prices/' + p_filename)
