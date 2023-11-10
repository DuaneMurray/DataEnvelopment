######################################################################
# LOAD LIBRARIES
import sys
import os
import math
import numpy as np
from sklearn.linear_model import LinearRegression
import shutil
from sqlalchemy import create_engine
from glob import glob
import requests
import pandas as pd
from pandas_market_calendars import get_calendar
import pandas_market_calendars as mcal
import datetime
from datetime import datetime
import mysql.connector


connection = mysql.connector.connect(host='localhost',
                             database='stockdata',
                             user='vsc',
                             password='blaster123')

# this will retun MySQLCursorPrepared object
#cursor = connection.cursor(prepared=True)


# USER, PW, AND DB ARE BEING IMPORTED FROM dbconfig.py FILE
db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
           .format(user = "vsc",
                   pw = "blaster123",
                   db = "stockdata"))  

# USING 'CREATE_ENGINE' FROM SQLALCHEMY TO MAKE THE DB CONNECTION
engine1 = create_engine(db_data).connect()
engine2 = create_engine(db_data).connect()

# CREATE A CURSORS TO THE DATABASE
cursor = connection.cursor(buffered=True)
mycursor = connection.cursor()

######################################################################
data = pd.DataFrame() # INIT EMPTY DATAFRAME OBJECT TO CONCAT FINAL OUTPUT
df = pd.DataFrame()

##########################################
# COMPARISON MARKET TO BENCHMARK AGAINST
market = '^GSPC'    # S&P 500
#market = '^DJI'     # DOW JONES
#market = '^IXIC'    # NASDAQ

######################################################################
# BUILD A QUERY TO THE DATABASE FOR SECURITIES 
# TO INCLUDE IN THE DEA BENCHMARK ANALYSIS STUDY SET:
# ("SELECT DISTINCT Sector FROM stock.securities;")
# SECTORS AVAILABLE FOR USE (ex: sector='Technology'):
#
# Financial Services
# Basic Materials
# Consumer Defensive
# Industrials
# Energy
# Healthcare
# Communication Services
# Consumer Cyclical
# Technology
# Real Estate
# Utilities

# LIST OF SECTORS TO PROCESS
sector_list = ["Financial Services", "Basic Materials", "Consumer Defensive", "Industrials", 
"Energy", "Healthcare", "Communication Services", "Consumer Cyclical", "Technology", "Real Estate",
"Utilities"]

#sector_list = ["Utilities"] # TEST DATA

#######################################################
# SET THE TIME FRAME FOR THE CALCULATIONS
year = '2015'   # YEAR TO PROCESS

# LEAP YEARS: 
# 2000, 2004, 2008, 2012, 2016, 2020, 2024
#
# January: 31 days
# February: 28 days and 29 in every leap year
# March: 31 days
# April: 30 days
# May: 31 days
# June: 30 days
# July: 31 days
# August: 31 days
# September: 30 days
# October: 31 days
# November: 30 days
# December: 31 days

month_start_dates = [year + '-01-01', year + '-02-01', year + '-03-01', year + '-04-01', year + '-05-01',
                     year + '-06-01', year + '-07-01', year + '-08-01', year + '-09-01', year + '-10-01',
                     year + '-11-01', year + '-12-01']

month_end_dates = [year + '-01-31', year + '-02-28', year + '-03-31', year + '-04-30', year + '-05-31',
                   year + '-06-30', year + '-07-31', year + '-08-31', year + '-09-30', year + '-10-31',
                   year + '-11-30', year + '-12-31']

counter = 0 # USED FOR DATE LIST INDEX ACCESS

for date_start in month_start_dates:
      
      # GET THE PRE-DEFINED END OF MONTH VALUES
      date_end = month_end_dates[counter]
      counter += 1

      # FIRST AND LAST TRADING DAYS FOR EACH HOLDING PERIOD
      first_trading_days = []
      last_trading_days = []

      # GET THE VALID BUSINESS TRADING DAYS OF THE MONTH
      us_calendar = get_calendar("BMF")
      valid_range = us_calendar.valid_days(start_date=date_start, end_date=date_end)

      first_trading_days.append(min(valid_range))
      last_trading_days.append(max(valid_range))

      # GET THE FIRST AND LAST TRADING DAYS OF THE MONTH
      first_trading_day = first_trading_days[0].strftime("%Y-%m-%d")
      last_trading_day = last_trading_days[0].strftime("%Y-%m-%d")

      # GET THE CURRENT FINANCIAL QUARTER
      q_date = pd.to_datetime(last_trading_day)
      quarter = 'Q' + str(q_date.quarter)

      # GET THE YEAR FOR EACH FINANCIAL QUARTER
      year = last_trading_days[0].strftime("%Y")

      #sys.exit("Breakpoint -- sys.exit()")


      # creating a date time object
      #my_date = pd.Timestamp(2022, 4, 29)

      # obtaing the quarter of the given year
      #print("The given date can be found in quarter ", my_date.quarter)

      ######################################################################
      # BUILD S&P 500 INDEX DATAFRAME FOR BENCHMARK RATIO BASELINE
      # GET THE PERCENT CHANGE OF THE COMPARISON MARKET FOR BETA AND RETURN RATE CALCULATIONS

      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN START DATE
      #query_roi_mkt_start = ("SELECT date, symbol, close FROM market_index "
      #        "WHERE symbol=%s AND date = %s")
      query_roi_mkt_start = ("SELECT date, symbol, close FROM market_index "
              "WHERE symbol=%s AND (date BETWEEN %s AND %s)")
      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN END DATE   
      #query_roi_mkt_end = ("SELECT date, symbol, close FROM market_index "
      #        "WHERE symbol=%s AND date = %s")
      query_roi_mkt_end = ("SELECT date, symbol, close FROM market_index "
              "WHERE symbol=%s AND (date BETWEEN %s AND %s)")

      # EXECUTE THE QUERY; GRAB THE MARKET INDEX VALUE FOR THE START DATE
      #cursor.execute(query_roi_mkt_start, (market, date_start))
      cursor.execute(query_roi_mkt_start, (market, first_trading_day, last_trading_day))
      sp500_start_result = cursor.fetchall()

      # EXECUTE THE QUERY; GRAB THE MARKET INDEX VALUE FOR THE END DATE
      #cursor.execute(query_roi_mkt_end, (market, date_end))
      cursor.execute(query_roi_mkt_end, (market, first_trading_day, last_trading_day))
      sp500_end_result = cursor.fetchall()

      # CALCULATE THE MARKET INDEX RATE OF RETURN FOR THE DATE RANGE VALUES
      #sp500_rate_of_return = (((sp500_end_result[0][2] - sp500_start_result[0][2]) / sp500_start_result[0][2]) * 100)
      sp500_rate_of_return = (((sp500_end_result[0][2] - sp500_end_result[-1][2]) / sp500_end_result[-1][2]))

      # PROCESS ALL SECTORS IN THE sector_list
      for market_symbol in sector_list:
            symbol_query = ("SELECT symbol FROM company_details WHERE symbol NOT LIKE '%-%' AND sector=%s")
            cursor.execute(symbol_query, (market_symbol,))
            my_symbol_result = cursor.fetchall()

            # LOOP THRU EACH SYMBOL RETURNED IN symbol_query SQL
            for x in my_symbol_result:

              # THE CURRENT SYMBOL TEXT - FOR CODE READABILITY
              current_symbol = x[0]
              #print(current_symbol)

              # QUERY TO GET THE STANDARD DEVIATION OVER THE DATE RANGE FOR THE STOCK PRICE
              query_sigma = ("SELECT STDDEV(close) FROM equity_prices "
                      "WHERE symbol=%s AND (date BETWEEN %s AND %s)")
                
              # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN START DATE 
              query_roi_start = ("SELECT date, symbol, close FROM equity_prices "
                      "WHERE symbol=%s AND date = %s")
                
              # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN END DATE 
              query_roi_end = ("SELECT date, symbol, close FROM equity_prices "
                      "WHERE symbol=%s AND date = %s")

              ############################################
              # GET DATA FOR SLOPE REGRESSION FOR BETA
              #
              stock_query = ("SELECT close FROM equity_prices "
                      "WHERE symbol=%s AND (date BETWEEN %s AND %s)")

              market_query = ("SELECT close FROM market_index "
                      "WHERE symbol=%s AND (date BETWEEN %s AND %s)")

              cursor.execute(stock_query, (current_symbol, date_start, date_end))
              myresult = cursor.fetchall()
              df_stock_query = pd.DataFrame(myresult)

              cursor.execute(market_query, (market, date_start, date_end))
              myresult = cursor.fetchall()
              df_market_query = pd.DataFrame(myresult)

                # IF DATA EXISTS FOR THE STOCK AND THE SIZE OF PRICE ARRAY = SIZE OF MARKET ARRAY
              if (not df_stock_query.empty and (df_stock_query.shape[0] == df_market_query.shape[0])):
                      stock_price_change = df_stock_query.pct_change()
                      market_price_change = df_market_query.pct_change()

                      stock_price_change.dropna(inplace=True)
                      market_price_change.dropna(inplace=True)

                      # Create arrays for x and y variables in the regression model
                      # Set up the model and define the type of regression
                      x = np.array(stock_price_change).reshape((-1,1)) # STOCK SYMBOL PERCENT CHANGE
                      y = np.array(market_price_change) # S&P 500 MARKET PERCENT CHANGE
                      model = LinearRegression().fit(x, y) # SOLVE THE MODEL

                      beta = model.coef_[0]

                      #cursor.execute(query_sigma, (current_symbol, date_start, date_end))
                      cursor.execute(query_sigma, (current_symbol, first_trading_day, last_trading_day))

                      # GET ALL THE RESULTS
                      myresult = cursor.fetchall()

                      # PLACE THE MYSQL OUTPUT RESULT LIST INTO A DATAFRAME OBJECT
                      df_sigma = pd.DataFrame(myresult)

                      # GET THE BEGINNING OF THE TIMEFRAME CLOSING PRICE
                      #cursor.execute(query_roi_start, (current_symbol, date_start))
                      cursor.execute(query_roi_start, (current_symbol, first_trading_day))
                      myresult_roi_start = cursor.fetchall()
                      df_start = pd.DataFrame(myresult_roi_start)

                      # GET THE ENDING OF THE TIMEFRAME CLOSING PRICE
                      #cursor.execute(query_roi_end, (current_symbol, date_end))
                      cursor.execute(query_roi_end, (current_symbol, last_trading_day))
                      myresult_roi_end = cursor.fetchall()
                      df_end = pd.DataFrame(myresult_roi_end)

                      # DROP ROWS WITH ANY EMPTY VALUES BEFORE PROCESSING
                      df_sigma.dropna(inplace=True)
                      df_start.dropna(inplace=True)
                      df_end.dropna(inplace=True)

                      if (not df_start.empty and  not df_end.empty):
                              rate_of_return = ((df_end[2] - df_start[2]) / df_start[2])

                              stock_beta_1 = (rate_of_return / sp500_rate_of_return)

                              stock_sigma = df_sigma[0][0]

                              df[0] = first_trading_day
                              df[1] = last_trading_day
                              df[2] = quarter
                              df[3] = year
                              df[4] = current_symbol
                              df[5] = market_symbol
                              df[6] = rate_of_return
                              df[7] = sp500_rate_of_return
                              df[8] = beta
                              df[9] = stock_sigma
                              df[10] = 'M'
                              df[11] = market

                              data = pd.concat([data, df])


# ADD COL NAMES AFTER DATAFRAME HAS BEEN BUILT
data.columns = ['StartDate', 'EndDate', 'Quarter', 'Year', 'Symbol', 'Industry', 'StockReturnRate', 'MarketReturnRate', 'Beta', 'Sigma', 'Period', 'MktIndex']
#print(data)                              

# REMOVE ANY ROWS THAT CONTAIN NaN VALUES FROM THE ANALYSIS
data.dropna(inplace=True)

#sys.exit("Breakpoint -- sys.exit()")
                
#data.to_csv('Beta-Output.csv', index=False)
data.to_sql(name='company_beta_sigma', con=engine2, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE

########################################################
# CLOSE THE DATABASE CONNECTIONS AND REFERENCE CURSORS
cursor.close()
mycursor.close()
connection.close()