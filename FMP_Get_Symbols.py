import requests
import pandas as pd

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '?apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# Exchange : ETF | MUTUAL_FUND | COMMODITY | INDEX | CRYPTO | FOREX | TSX | AMEX | NASDAQ | NYSE | EURONEXT
exchange = 'NASDAQ'
#exchange = 'NYSE'
#exchange = 'AMEX'

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v3/symbol/'

#debug_output = pd.DataFrame() # CREATE EMPTY DATAFRAME FOR OUTPUT TO SCREEN

#########
data_directory = "Data/"        # DIRECTORY NAME UNDER THIS SCRIPTS LOCATION

resp = requests.get(base_url + exchange + api_token)
resp.raise_for_status()

df = pd.DataFrame(resp.json()) # PUT THE JSON RESULTS INTO A DATAFRAME

filename = exchange + '.csv'
df.to_csv(data_directory + filename, index=False)

