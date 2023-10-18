# RATIOS
#
# symbol=string
# period=annual, quarter
# limit=number
# 
# https://financialmodelingprep.com/api/v3/ratios/AAPL?period=quarter

import requests
import pandas as pd

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '&apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/ratios/'  # ADD SYMBOL ON END OF URL

debug_output = pd.DataFrame() # CREATE EMPTY DATAFRAME FOR OUTPUT TO SCREEN

#########
period = 'quarter'              # OPTIONS: quarter, annual
limit = '140'                   # MAX NUMBER OF PERIODS TO RETURN: MAX = 140
data_directory = "Data/"        # DIRECTORY NAME UNDER THIS SCRIPTS LOCATION
output_file_directory ="Stock-Fundamentals/Quarterly/"  # DIRECTORY NAME TO STORE OUTPUT CSV FILES
stock_list = pd.read_csv(data_directory + "Symbols-TEST.csv") # LIST OF SYMBOLS
##########

# LOOP THROUGH THE LIST OF SYMBOLS INPUT FROM THE DEFINED stock_list FILE
for x in stock_list['Symbol']:
  # GET FINANCIAL RATIOS FOR FUNDAMENTAL ANALYSIS - QUICK RATIO, ETC
  resp = requests.get(base_url + x + '?period=' + period + '&limit=' + limit + api_token)
  resp.raise_for_status()

  company_ratios = pd.DataFrame(resp.json()) # PUT THE JSON RESULTS INTO A DATAFRAME
  company_ratios['period'] = period

  filename = x + '-Company-Ratios-Quarterly.csv'       # DEFINE THE FILENAME FOR CSV OUTPUT
  
  # GENERATE A CSV OUTPUT FILE IGNORING THE ROW INDEX NUMBERS
  company_ratios.to_csv(data_directory + output_file_directory + filename, index=False)
  
  # CONCATENTATE DATAFRAMES FOR DISPLAY OUTPUT
  debug_output = pd.concat([debug_output, company_ratios], ignore_index=True)
  
# CONVERT EPOCH DATE FORMAT
#debug_output['date'] = pd.to_datetime(debug_output['date']/1000, unit="s")
print(debug_output) # OUTPUT RESULTS TO SCREEN