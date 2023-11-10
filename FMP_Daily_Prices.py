# DAILY CHART - HISTORICAL PRICES
# 
# symbol=string
# from=date	2023-10-11
# to=date		2023-01-09
# 
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL

import sys

import os
import mysql.connector
import shutil
from sqlalchemy import create_engine
from glob import glob
import requests
import pandas as pd

# USER, PW, AND DB ARE BEING IMPORTED FROM dbconfig.py FILE
db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
           .format(user = "vsc",
                   pw = "blaster123",
                   db = "stockdata"))  

# USING 'CREATE_ENGINE' FROM SQLALCHEMY TO MAKE THE DB CONNECTION
engine1 = create_engine(db_data).connect()
engine2 = create_engine(db_data).connect()

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '&apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/historical-price-full/'  # ADD SYMBOL ON END OF URL

#debug_output = pd.DataFrame() # CREATE EMPTY DATAFRAME FOR OUTPUT TO SCREEN

#########
start_date = '1991-01-01'
end_date = ''

##########
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE symbol="AAPL" ORDER BY symbol', engine1)

#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="AMEX" AND symbol NOT LIKE "%-%" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="NYSE" AND symbol NOT LIKE "%-%" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="NASDAQ" AND symbol NOT LIKE "%-%" ORDER BY symbol', engine1)

#################################
# SECTORS
#################################
#
## Financial Services
## Basic Materials
## Consumer Defensive
## Industrials
## Energy
## Healthcare
## Communication Services
## Consumer Cyclical
## Technology
## Real Estate
## Utilities
#
# VIEW: company_data_set
#
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Financial Services" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Basic Materials" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Consumer Defensive" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Industrials" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Energy" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Healthcare" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Communication Services" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Consumer Cyclical" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Technology" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Real Estate" ORDER BY symbol', engine1)
stock_list = pd.read_sql('SELECT DISTINCT symbol FROM company_data_set WHERE sector="Utilities" ORDER BY symbol', engine1)

##########
#sys.exit("Breakpoint -- sys.exit()")


for x in stock_list['symbol']:
  
  # GET PRICE HISTORY FOR THE CURRENT STOCK IN THE LIST
  resp = requests.get(base_url + x + '?from='+ start_date +'&to='+ end_date + api_token)
  resp.raise_for_status()
  
  df = resp.json()                    # GET THE JSON DATA FROM THE API

  # MAKE SURE THE DATAFRAME HAS "historical" COLUMN
  if "historical" in list(df):
    df2 = pd.DataFrame(df["historical"]) # PARSE THE HISTORICAL JSON SECTION
  
    df2['symbol'] = x                      # ADD THE STOCK SYMBOL TO THE DATAFRAME
    
    df2.to_sql(name='equity_prices', con=engine2, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE


  # VIEW NESTED JSON DATA RECEIVED FROM API - DEBUG OUTPUT
  #print("Symbol:", data["symbol"])
  #print("Historical Data:")
  #for entry in data["historical"]:
  #  print(f"Date: {entry['date']}")
  #  print(f"Open: {entry['open']}")
  #  print(f"High: {entry['high']}")
  #  print(f"Low: {entry['low']}")
  #  print(f"Close: {entry['close']}")
  #  print(f"Volume: {entry['volume']}")
  #  print(f"Change Percent: {entry['changePercent']}")
  #  print(f"Label: {entry['label']}")
  #  print()