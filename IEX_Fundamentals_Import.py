#################################################################################
# KEY VARIABLES TO USE IN THE DEA MODEL
#
# From Case Study (Mixed Technical and Fundamentals)
#
# Inputs(x): 
#	Debt to Equity, Price to Book, Sigma, Beta
# Outputs(y): (4 different analysis runs)
#	1-month Return, Net Profit Margin, EPS, Return on Asset, Return on Equity
#	1-year Return, Net Profit Margin, EPS, Return on Asset, Return on Equity
#	3-year Return, Net Profit Margin, EPS, Return on Asset, Return on Equity
#	5-year Return, Net Profit Margin, EPS, Return on Asset, Return on Equity

########################################################
# ACCESS THE IEX CLOUD DATA FOR STOCK ANALYSIS
# https://iexcloud.io/docs/api/#excel-how-to
########################################################
import requests
import pandas as pd

########################################################
# IEX Cloud API Keys:
# https://iexcloud.io/console/home
# Publishable: pk_56f07a5d1b424234ac83bb932eb56eff
# Secret: sk_1b32b35bb3514c2eac4bb01139f61c1a
#########################################################
secret_token = "sk_1b32b35bb3514c2eac4bb01139f61c1a"
publishable_key = "pk_56f07a5d1b424234ac83bb932eb56eff"
params = {'token': secret_token}

# IEX Cloud REST API URLs
base_url = 'https://cloud.iexapis.com/v1'
sandbox_url = 'https://sandbox.iexapis.com/stable'


symbol_list = "" # CREATE EMPTY STRING VAR
fundamental_valuations = pd.DataFrame() # CREATE EMPTY DATAFRAME

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

stock_list = pd.read_csv("US_NASDAQ_Medium_MarketCap_Stocks.csv") # 1170 Symbols
sector_directory = "MarketCap/Medium/"

###stock_list = pd.read_csv("US_NASDAQ_Mega_MarketCap_Stocks.csv") # 47 Symbols
###sector_directory = "MarketCap/Mega/"

#stock_list = pd.read_csv("US_NASDAQ_Micro_MarketCap_Stocks.csv") # 1241 Symbols
#sector_directory = "MarketCap/Micro/"

#stock_list = pd.read_csv("US_NASDAQ_Nano_MarketCap_Stocks.csv") # 2199 Symbols
#sector_directory = "MarketCap/Nano/"

##############
# N. AMERICA
##############

#stock_list = pd.read_csv("US_NASDAQ_North_America_Stocks.csv") # 2199 Symbols
#sector_directory = "NorthAmerica/"

#################################################################################
###stock_list = pd.read_csv("Symbols.csv") # TESTING DATA FILE - 3 Symbols
#################################################################################

for x in stock_list['Symbol']:
  symbol_list = symbol_list + x + ',' # BUILD A COMMA SEP LIST IN A STRING
  # GET FINANCIAL RATIOS FOR FUNDAMENTAL ANALYSIS - QUICK RATIO, ETC
  resp = requests.get(base_url+'/time-series/FUNDAMENTAL_VALUATIONS/'+x+'/annual?from=2015-01-01', params=params)
  resp.raise_for_status()
  fundamental_val = pd.DataFrame(resp.json())
  filename = x + '-Fundamental-Valuation.csv'
  fundamental_val.to_csv('Fundamentals/' + sector_directory + filename)
  fundamental_valuations = pd.concat([fundamental_valuations,fundamental_val], ignore_index=True)
  
fundamental_valuations['date'] = pd.to_datetime(fundamental_valuations['date']/1000, unit="s")

compiled_list = pd.DataFrame()

#for x in stock_list['Symbol']:
#    filename = 'Fundamentals/' + x + '-Fundamental-Valuation.csv'
#    stock_to_process = pd.read_csv(filename)
#    compiled_list.concat[stock_to_process]

print(fundamental_valuations)


