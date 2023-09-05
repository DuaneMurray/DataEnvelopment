import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import os

secret_token = "sk_1b32b35bb3514c2eac4bb01139f61c1a"
publishable_key = "pk_56f07a5d1b424234ac83bb932eb56eff"

os.environ["IEX_API_KEY"] = secret_token

############################################################
# DATA SOURCE FILES
#
# UN-COMMENT SECTION TO PROCESS - ONE SECTOR AT A TIME
############################################################

###stock_list = pd.read_csv("US_NASDAQ_Consumer_Discretionary_Stocks.csv") # 1179 Symbols
###sector_directory = "ConsumerDiscretionary/"

###stock_list = pd.read_csv("US_NASDAQ_Consumer_Staples_Stocks.csv") # 151 Symbols
###sector_directory = "ConsumerStaples/"

###stock_list = pd.read_csv("US_NASDAQ_Energy_Stocks.csv") # 211 Symbols
###sector_directory = "Energy/"

###stock_list = pd.read_csv("US_NASDAQ_Financial_Stocks.csv") # 1996 Symbols
###sector_directory = "Financial/"

###stock_list = pd.read_csv("US_NASDAQ_Healthcare_Stocks.csv") # 1288 Symbols
###sector_directory = "Healthcare/"

###stock_list = pd.read_csv("US_NASDAQ_Industirals_Stocks.csv") # 564 Symbols
###sector_directory = "Industrials/"

###stock_list = pd.read_csv("US_NASDAQ_Basic_Materials_Stocks.csv") # 101 Symbols
###sector_directory = "Materials/"

###stock_list = pd.read_csv("US_NASDAQ_RealEstate_Stocks.csv") # 265 Symbols
###sector_directory = "RealEstate/"

###stock_list = pd.read_csv("US_NASDAQ_Technology_Stocks.csv") # 637 Symbols
###sector_directory = "Technology/"

###stock_list = pd.read_csv("US_NASDAQ_Telecom_Stocks.csv") # 96 Symbols
###sector_directory = "Telecom/"

###stock_list = pd.read_csv("US_NASDAQ_Utilities_Stocks.csv") # 177 Symbols
###sector_directory = "Utilities/"

###############
# MARKET CAP
###############

###stock_list = pd.read_csv("US_NASDAQ_Large_MarketCap_Stocks.csv") # 806 Symbols
###sector_directory = "MarketCap/Large/"

#stock_list = pd.read_csv("US_NASDAQ_Medium_MarketCap_Stocks.csv") # 1170 Symbols
#sector_directory = "MarketCap/Medium/"

#stock_list = pd.read_csv("US_NASDAQ_Mega_MarketCap_Stocks.csv") # 47 Symbols
#sector_directory = "MarketCap/Mega/"

#stock_list = pd.read_csv("US_NASDAQ_Micro_MarketCap_Stocks.csv") # 1241 Symbols
#sector_directory = "MarketCap/Micro/"

#stock_list = pd.read_csv("US_NASDAQ_Nano_MarketCap_Stocks.csv") # 2199 Symbols
#sector_directory = "MarketCap/Nano/"

##############
# N. AMERICA
##############

stock_list = pd.read_csv("US_NASDAQ_North_America_Stocks.csv") # 2199 Symbols
sector_directory = "NorthAmerica/"

#################################################################################
###stock_list = pd.read_csv("Symbols.csv") # TESTING DATA FILE - 3 Symbols
#################################################################################

start = datetime(2015,1,1)
end = datetime(2023,7,27)

for x in stock_list['Symbol']:
    df = web.DataReader(x, 'iex', start, end)
    df['Symbol'] = x
    filename = x + '-Price-History.csv'
    df.to_csv('Fundamentals/' + sector_directory + filename)
