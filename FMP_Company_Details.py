# COMPANY OUTLOOK
# Provides combined JSON for all financial data including company info:
# https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL
#
# ** COMPANY PROFILE **
# A summary of important company information, including price, beta, market capitalization,
# description, headquarters, sector, industry, and more
#
# API: https://financialmodelingprep.com/api/v3/profile/AAPL

import requests
import pandas as pd

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '?apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/profile/'  # ADD SYMBOL ON END OF URL

#debug_output = pd.DataFrame() # CREATE EMPTY DATAFRAME FOR OUTPUT TO SCREEN

#########
data_directory = "Data/"        # DIRECTORY NAME UNDER THIS SCRIPTS LOCATION
output_file_directory ="Stock-Details/"  # DIRECTORY NAME TO STORE OUTPUT CSV FILES

#stock_list = pd.read_csv(data_directory + "Symbols-TEST.csv") # LIST OF SYMBOLS
#stock_list = pd.read_csv(data_directory + "Symbols-Communication-Services.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Consumer-Discretionary.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Consumer-Staples.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Energy.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Financials.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Health-Care.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Industrials.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Information-Technology.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Materials.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Real-Estate.csv")
#stock_list = pd.read_csv(data_directory + "Symbols-Utilities.csv")

stock_list = pd.read_csv(data_directory + "NASDAQ.csv")
#stock_list = pd.read_csv(data_directory + "NYSE.csv")
#stock_list = pd.read_csv(data_directory + "AMEX.csv")
##########

# LOOP THROUGH THE LIST OF SYMBOLS INPUT FROM THE DEFINED stock_list FILE
for x in stock_list['Symbol']:
  # GET FINANCIAL RATIOS FOR FUNDAMENTAL ANALYSIS - QUICK RATIO, ETC
  resp = requests.get(base_url + x + api_token)
  resp.raise_for_status()

  company_details = pd.DataFrame(resp.json()) # PUT THE JSON RESULTS INTO A DATAFRAME
  filename = x + '-Company-Details.csv'       # DEFINE THE FILENAME FOR CSV OUTPUT
  
  # GENERATE A CSV OUTPUT FILE IGNORING THE ROW INDEX NUMBERS
  company_details.to_csv(data_directory + output_file_directory + filename, index=False)
  
  # CONCATENTATE DATAFRAMES FOR DISPLAY OUTPUT
  #debug_output = pd.concat([debug_output, company_details], ignore_index=True)
  
# CONVERT EPOCH DATE FORMAT
#debug_output['date'] = pd.to_datetime(debug_output['date']/1000, unit="s")
#print(debug_output) # OUTPUT RESULTS TO SCREEN