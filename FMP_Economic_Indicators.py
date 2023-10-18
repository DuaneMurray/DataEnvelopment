# ECONOMIC INDICATORS
#
# name=string	GDP, Real GDP, Unemployment rate, more...
# from=date	2019-10-10
# to=date		2021-11-10
#
# https://financialmodelingprep.com/api/v4/economic?name=GDP

# names:
# GDP, realGDP, nominalPotentialGDP, realGDPPerCapita, federalFunds, 
# CPI, inflationRate, inflation, retailSales, consumerSentiment, 
# durableGoods, unemploymentRate, totalNonfarmPayroll, initialClaims, 
# industrialProductionTotalIndex, newPrivatelyOwnedHousingUnitsStartedTotalUnits, 
# totalVehicleSales, retailMoneyFunds, smoothedUSRecessionProbabilities, 
# 3MonthOr90DayRatesAndYieldsCertificatesOfDeposit, 
# commercialBankInterestRateOnCreditCardPlansAllAccounts, 
# 30YearFixedRateMortgageAverage, 15YearFixedRateMortgageAverage

import requests
import pandas as pd

# FMP API TOKEN MAY NEED TO USE '&' OR '?' AT BEGINING DEPENDING ON API ENDPOINT
api_token = '&apikey=806a23dbb33fc1793a282fde9990c045' # ADD TO END OF REST API URL

# FMP REST API URLs
base_url = 'https://financialmodelingprep.com/api/v4/economic/'  # ADD SYMBOL ON END OF URL

#debug_output = pd.DataFrame() # CREATE EMPTY DATAFRAME FOR OUTPUT TO SCREEN

#########
start_date = '1998-01-01'
end_date = ''
data_directory = "Data/"
output_file_directory ="Economic-Reports/"
stock_list = pd.read_csv(data_directory + "Symbols-TEST.csv") # 1170 Symbols
econ_report_list = [
'GDP', 'realGDP', 'nominalPotentialGDP', 'realGDPPerCapita', 'federalFunds', 
'CPI', 'inflationRate', 'inflation', 'retailSales', 'consumerSentiment', 
'durableGoods', 'unemploymentRate', 'totalNonfarmPayroll', 'initialClaims', 
'industrialProductionTotalIndex', 'newPrivatelyOwnedHousingUnitsStartedTotalUnits', 
'totalVehicleSales', 'retailMoneyFunds', 'smoothedUSRecessionProbabilities', 
'3MonthOr90DayRatesAndYieldsCertificatesOfDeposit', 
'commercialBankInterestRateOnCreditCardPlansAllAccounts', 
'30YearFixedRateMortgageAverage', '15YearFixedRateMortgageAverage']
##########

################
# NEED TO CHANGE TO LOOP THROUGH A LIST OF THE ECONOMIC DATA NEEDED: name
################
for name in econ_report_list:
  
  # GET PRICE HISTORY FOR THE CURRENT STOCK IN THE LIST
  #resp = requests.get(base_url + x + '?from='+ start_date +'&to='+ end_date + api_token)
  resp = requests.get(base_url + '?name=' + name + '&from='+ start_date +'&to='+ end_date + api_token)
  resp.raise_for_status()
  
  data = resp.json()                    # GET THE JSON DATA FROM THE API
  df = pd.DataFrame(data)               # PARSE THE HISTORICAL JSON SECTION
  df['name'] = name                      # ADD THE STOCK SYMBOL TO THE DATAFRAME

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
  
  filename = 'Economic-Indicator-' + name + '.csv'

  # GENERATE A CSV OUTPUT FILE IGNORING THE ROW INDEX NUMBERS
  df.to_csv(data_directory + output_file_directory + filename, index=False)

  #debug_output = pd.concat([debug_output, df], ignore_index=True)

# CONVERT EPOCH DATE FORMAT IF NEEDED
#debug_output['date'] = pd.to_datetime(debug_output['date']/1000, unit="s")
#print(debug_output) # OUTPUT RESULTS TO SCREEN