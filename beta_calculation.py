import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine
import pandas as pd
from pandas_market_calendars import get_calendar
import pandas_market_calendars as mcal
import datetime
from datetime import datetime
import mysql.connector


# CREATE A CONNECTION TO THE MYSQL DATABASE
connection = mysql.connector.connect(host='localhost',
                             database='stockdata',
                             user='vsc',
                             password='blaster123')

# ALTERNATIVE CONNECTION THE THE MYSQL DATABASE
db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
           .format(user = "vsc",
                   pw = "blaster123",
                   db = "stockdata"))  

# USING 'CREATE_ENGINE' FROM SQLALCHEMY TO MAKE THE DB CONNECTION
engine1 = create_engine(db_data).connect()
engine2 = create_engine(db_data).connect()

# CREATE CURSORS TO THE DATABASE
cursor = connection.cursor(buffered=True)
mycursor = connection.cursor()

######################################################################
data = pd.DataFrame()   # INIT EMPTY DATAFRAME OBJECT TO CONCAT FINAL OUTPUT
df = pd.DataFrame()     # TEMP DATAFRAME FOR BULDING data OUTPUT DATAFRAME

##################################################
# COMPARISON MARKET TO BENCHMARK BETA VAL AGAINST
market = '^GSPC'     # S&P 500
#market = '^DJI'     # DOW JONES
#market = '^IXIC'    # NASDAQ

######################################################################
# BUILD A QUERY TO THE DATABASE FOR SECURITIES 
# TO INCLUDE IN THE DEA BENCHMARK ANALYSIS STUDY SET:
# ("SELECT DISTINCT Sector FROM stock.securities;")

# LIST OF SECTORS TO PROCESS
sector_list = ["Financial Services", "Basic Materials", "Consumer Defensive", "Industrials", 
"Energy", "Healthcare", "Communication Services", "Consumer Cyclical", "Technology", "Real Estate",
"Utilities"]

#sector_list = ["Utilities"] # TEST DATA

#######################################################
# SET THE TIME FRAME FOR THE CALCULATIONS
# LEAP YEARS: 
# 2000, 2004, 2008, 2012, 2016, 2020, 2024

# YEAR TO PROCESS
#year = '2015'
#year = '2016' 
#year = '2017'
#year = '2018'
#year = '2019'
#year = '2020'
#year = '2021'
#year = '2022'
year = '2023'  # FULL YEAR DATA NOT COMPLETE AS OF 11/11/23

month_start_dates = [year + '-01-01', year + '-02-01', year + '-03-01', year + '-04-01', year + '-05-01',
                     year + '-06-01', year + '-07-01', year + '-08-01', year + '-09-01', year + '-10-01',
                     year + '-11-01', year + '-12-01']

month_end_dates = [year + '-01-31', year + '-02-28', year + '-03-31', year + '-04-30', year + '-05-31',
                   year + '-06-30', year + '-07-31', year + '-08-31', year + '-09-30', year + '-10-31',
                   year + '-11-30', year + '-12-31']

counter = 0 # USED FOR DATE LIST INDEX ACCESS

# LOOP THROUGH ALL MONTHS OF THE DEFINED YEAR, CALCULATE BETA AND SIGMA
# AND INSERT THE VALUES INTO A MYSQL DATABASE TABLE
for date_start in month_start_dates:
      
      # GET THE PRE-DEFINED END OF MONTH VALUES
      date_end = month_end_dates[counter] # STARTS AT ZERO (0)
      counter += 1  # INCREMENT THE INDEX ACCESS COUNTER

      # DEFINE FIRST AND LAST TRADING DAYS LISTS FOR EACH HOLDING PERIOD
      first_trading_days = []
      last_trading_days = []

      # GET THE VALID BUSINESS TRADING DAYS OF THE MONTH FROM MARKET CALENDAR
      us_calendar = get_calendar("BMF")
      valid_range = us_calendar.valid_days(start_date=date_start, end_date=date_end)

      first_trading_days.append(min(valid_range)) # FIRST DAY
      last_trading_days.append(max(valid_range))  # LAST DAY

      # GET THE FIRST AND LAST TRADING DAYS OF THE MONTH IN CORRECT DATE FORMAT
      first_trading_day = first_trading_days[0].strftime("%Y-%m-%d")
      last_trading_day = last_trading_days[0].strftime("%Y-%m-%d")

      # GET THE CURRENT FINANCIAL QUARTER - PANDAS DATETIME.QUARTER
      q_date = pd.to_datetime(last_trading_day)
      quarter = 'Q' + str(q_date.quarter)

      # GET THE YEAR FOR EACH FINANCIAL QUARTER
      year = last_trading_days[0].strftime("%Y")

      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN START DATE
      query_roi_mkt_start = ("SELECT date, symbol, close FROM market_index "
              "WHERE symbol=%s AND (date BETWEEN %s AND %s)")
      
      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN END DATE   
      query_roi_mkt_end = ("SELECT date, symbol, close FROM market_index "
              "WHERE symbol=%s AND (date BETWEEN %s AND %s)")

      # EXECUTE THE QUERY; GRAB THE MARKET INDEX VALUE FOR THE START DATE
      cursor.execute(query_roi_mkt_start, (market, first_trading_day, last_trading_day))
      sp500_start_result = cursor.fetchall()

      # EXECUTE THE QUERY; GRAB THE MARKET INDEX VALUE FOR THE END DATE
      cursor.execute(query_roi_mkt_end, (market, first_trading_day, last_trading_day))
      sp500_end_result = cursor.fetchall()

      # CALCULATE THE MARKET INDEX RATE OF RETURN FOR THE FIRST/LAST DATE RANGE VALUES
      # IN DECMAL FORM, MULTIPLY BY 100 IF NEEDED IN PERCENTAGE FORM
      sp500_rate_of_return = (((sp500_end_result[0][2] - sp500_end_result[-1][2]) / sp500_end_result[-1][2]))

      # PROCESS AND LOOP THROUGH ALL SECTORS IN THE sector_list
      for market_symbol in sector_list:
            
            # GET ALL STOCK SYMBOLS FOR THE GIVEN SECTOR THAT ARE NOT DERIVATIVES (-W, etc)
            symbol_query = ("SELECT symbol FROM company_details WHERE symbol NOT LIKE '%-%' AND sector=%s")
            cursor.execute(symbol_query, (market_symbol,))
            my_symbol_result = cursor.fetchall()

            # LOOP THRU EACH SYMBOL RETURNED IN symbol_query SQL
            for new_symbol in my_symbol_result:

              # THE CURRENT SYMBOL TEXT - FOR CODE READABILITY
              current_symbol = new_symbol[0]

              ###############################################
              # GET DATA FOR SLOPE REGRESSION - BETA VALUE
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
              # BOTH LISTS NEED TO BE THE SAME SHAPE (ROWS IN THIS CASE)
              if (not df_stock_query.empty and (df_stock_query.shape[0] == df_market_query.shape[0])):
                      stock_price_change = df_stock_query.pct_change()
                      market_price_change = df_market_query.pct_change()
                      
                      # REMOVE ALL ROWS THAT CONTAIN NAN VALUES
                      stock_price_change.dropna(inplace=True)
                      market_price_change.dropna(inplace=True)

                      ################################################################
                      # CREATE ARRAYS FOR x AND y VARIABLES FOR THE REGRESSION MODEL
                      # CALCUATE THE BETA VALUE FOR THE GIVEN STOCK AND MARKET BENCHMARK
                      x = np.array(stock_price_change).reshape((-1,1)) # STOCK SYMBOL PERCENT CHANGE
                      y = np.array(market_price_change) # S&P 500 MARKET PERCENT CHANGE
                      model = LinearRegression().fit(x, y) # SOLVE THE MODEL
                      beta = model.coef_[0]  # THE SLOPE VALUE = BETA VALUE

                      # QUERY TO GET THE STANDARD DEVIATION OVER THE DATE RANGE FOR THE STOCK PRICE
                      query_sigma = ("SELECT STDDEV(close) FROM equity_prices "
                                     "WHERE symbol=%s AND (date BETWEEN %s AND %s)")
                      cursor.execute(query_sigma, (current_symbol, first_trading_day, last_trading_day))
                      myresult = cursor.fetchall() # GET ALL THE RESULTS

                      # PLACE THE MYSQL RESULT LIST INTO A DATAFRAME OBJECT
                      df_sigma = pd.DataFrame(myresult)

                      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN START DATE 
                      query_roi_start = ("SELECT date, symbol, close FROM equity_prices "
                                         "WHERE symbol=%s AND date = %s")
                            
                      # GET THE BEGINNING OF THE TIMEFRAME CLOSING PRICE
                      cursor.execute(query_roi_start, (current_symbol, first_trading_day))
                      myresult_roi_start = cursor.fetchall()
                      df_start = pd.DataFrame(myresult_roi_start)

                      # QUERY TO GET THE MARKET INDEX VALUE AT A GIVEN END DATE 
                      query_roi_end = ("SELECT date, symbol, close FROM equity_prices "
                                       "WHERE symbol=%s AND date = %s")
              
                      # GET THE ENDING OF THE TIMEFRAME CLOSING PRICE
                      cursor.execute(query_roi_end, (current_symbol, last_trading_day))
                      myresult_roi_end = cursor.fetchall()
                      df_end = pd.DataFrame(myresult_roi_end)

                      # DROP ROWS WITH ANY EMPTY VALUES BEFORE PROCESSING
                      df_sigma.dropna(inplace=True)
                      df_start.dropna(inplace=True)
                      df_end.dropna(inplace=True)

                      # IF VALID STARTING AND ENDING DATES ARE AVAILABLE FOR THE STOCK
                      if (not df_start.empty and  not df_end.empty):
                              
                              # CALCUALTE THE STOCK RATE OF RETURN FOR THE PERIOD (MONTH)
                              rate_of_return = ((df_end[2] - df_start[2]) / df_start[2])

                              # ALTERNATIVE BETA CALCULATION METHOD
                              stock_beta_1 = (rate_of_return / sp500_rate_of_return)
                              
                              # GET THE STANDARD DEVIATION VALUE FOR CLOSE PRICES
                              stock_sigma = df_sigma[0][0]
                              
                              # SET THE VALUES FOR THE OUTPUT DATAFRAME
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
                              
                              # CONCATENATE THE NEW DATAFRAME ROW WITH THE FULL OUTPUT DATAFRAME
                              data = pd.concat([data, df])


# ADD COL NAMES FOR DATAFRAME THAT HAS BEEN BUILT
data.columns = ['StartDate', 'EndDate', 'Quarter', 'Year', 'Symbol', 'Industry', 'StockReturnRate', 'MarketReturnRate', 'Beta', 'Sigma', 'Period', 'MktIndex']

# REMOVE ANY ROWS THAT CONTAIN NaN VALUES FROM THE ANALYSIS
data.dropna(inplace=True)

# OUTPUT TO CSV FILE
#data.to_csv('Beta-Output.csv', index=False)

# OUTPUT DIRECTLY TO MYSQL DATABASE
data.to_sql(name='company_beta_sigma', con=engine2, chunksize=5000, if_exists='append') # ADD DATA TO EXISTING TABLE

########################################################
# CLOSE THE DATABASE CONNECTIONS AND REFERENCE CURSORS
cursor.close()
mycursor.close()
connection.close()

#sys.exit("Breakpoint -- sys.exit()") # BREAKPOINT METHOD