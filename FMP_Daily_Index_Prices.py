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
#base_url = 'https://financialmodelingprep.com//api/v3/quotes/index/'         # SHOW ALL MARKET INDICIES

# INDEX SYMBOLS (%5E = ^): 
# S&P500:       %5EGSPC
# DOW Jones:    %5EDJI
# NASDAQ:       %5EIXIC

#########
start_date = '1998-01-01'
end_date = ''
stock_list = ["^GSPC", "^DJI", "^IXIC"]
##########

#sys.exit("Breakpoint -- sys.exit()")

for x in stock_list:
  
  # GET PRICE HISTORY FOR THE CURRENT STOCK IN THE LIST
  resp = requests.get(base_url + x + '?from='+ start_date +'&to='+ end_date + api_token)
  resp.raise_for_status()
  
  df = resp.json()                    # GET THE JSON DATA FROM THE API

  # MAKE SURE THE DATAFRAME HAS "historical" COLUMN
  if "historical" in list(df):
    df2 = pd.DataFrame(df["historical"]) # PARSE THE HISTORICAL JSON SECTION
  
    df2['symbol'] = x                      # ADD THE STOCK SYMBOL TO THE DATAFRAME
    
    df2.to_sql(name='market_index', con=engine2, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE