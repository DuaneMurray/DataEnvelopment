###################################################
# GET ALL SYMBOLS FOR THE DEFINED STOCK EXCHANGE
# INSERT INTO stockdata.exchange_symbols TABLE
###################################################

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
engine = create_engine(db_data).connect()

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '?apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/symbol/'

############################################################################################################
# Exchange : ETF | MUTUAL_FUND | COMMODITY | INDEX | CRYPTO | FOREX | TSX | AMEX | NASDAQ | NYSE | EURONEXT
############################################################################################################
#exchange = 'NASDAQ'
#exchange = 'NYSE'
#exchange = 'AMEX'
#exchange = 'ETF'
#exchange = 'COMMODITY'
#exchange ='INDEX'
#############################################################################################################

resp = requests.get(base_url + exchange + api_token)
resp.raise_for_status()

df = pd.DataFrame(resp.json()) # PUT THE JSON RESULTS INTO A DATAFRAME

# IMPORT DATAFRAME INTO SQL DATABASE
# name = 'datbase_tablename', if_exists='append' MEANS: CREATES NEW TABLE, OTHERWISE APPEND DATA
#
#df.to_sql(name='company_details', con=engine, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE
df.to_sql(name='exchange_symbols', con=engine, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE
