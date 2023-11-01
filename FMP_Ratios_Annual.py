# RATIOS
#
# symbol=string
# period=annual, quarter
# limit=number
# 
# https://financialmodelingprep.com/api/v3/ratios/AAPL?period=quarter

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
base_url = 'https://financialmodelingprep.com/api/v3/ratios/'  # ADD SYMBOL ON END OF URL

#########
period = 'annual'              # OPTIONS: quarter, annual
limit = '35'                   # MAX NUMBER OF PERIODS TO RETURN: MAX = 140
##########

##########
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE symbol="AAPL" ORDER BY symbol', engine1)

stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="AMEX" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="NYSE" ORDER BY symbol', engine1)
#stock_list = pd.read_sql('SELECT DISTINCT symbol FROM exchange_symbols WHERE exchange="NASDAQ" ORDER BY symbol', engine1)
##########


# LOOP THROUGH THE LIST OF SYMBOLS INPUT FROM THE DEFINED stock_list FILE
for x in stock_list['symbol']:

  # GET FINANCIAL RATIOS FOR FUNDAMENTAL ANALYSIS - QUICK RATIO, ETC
  resp = requests.get(base_url + x + '?period=' + period + '&limit=' + limit + api_token)
  resp.raise_for_status()

  df = pd.DataFrame(resp.json()) # PUT THE JSON RESULTS INTO A DATAFRAME

  df.to_sql(name='company_ratios', con=engine2, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE
