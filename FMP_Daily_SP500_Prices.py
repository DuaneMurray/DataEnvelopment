# DAILY CHART - HISTORICAL PRICES
# 
# symbol=string
# from=date	2023-10-11
# to=date		2023-01-09
# 
# https://financialmodelingprep.com/api/v3/historical-price-full/AAPL

import requests
import pandas as pd

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '&apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/historical-price-full/'  # ADD SYMBOL ON END OF URL
#base_url = 'https://financialmodelingprep.com//api/v3/quotes/index/'         # SHOW ALL MARKET INDICIES
# INDEX SYMBOLS: %5EGSPC,%5EDJI,%5EIXIC

#########
start_date = '1998-01-01'
end_date = ''
data_directory = "Data/"
output_file_directory ="Indicies/"
#stock_list = pd.read_csv(data_directory + "Symbols-TEST.csv") # 1170 Symbols
##########

# GET PRICE HISTORY FOR THE INDEX IN THE resp URL
resp = requests.get(base_url + '^GSPC' + '?from='+ start_date +'&to='+ end_date + api_token)
resp.raise_for_status()
 
data = resp.json()                    # GET THE JSON DATA FROM THE API
df = pd.DataFrame(data["historical"]) # PARSE THE HISTORICAL JSON SECTION
df['symbol'] = 'SP500'                # ADD THE STOCK SYMBOL TO THE DATAFRAME

filename = 'SP500-Historical-Prices.csv'

# GENERATE A CSV OUTPUT FILE IGNORING THE ROW INDEX NUMBERS
df.to_csv(data_directory + output_file_directory + filename, index=False)