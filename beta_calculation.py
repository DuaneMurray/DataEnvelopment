######################################################################
# LOAD LIBRARIES
import math
import mysql.connector
#import datetime
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

######################################################################
# SET DATE RANGE FOR ANALYSIS - THIS SHOULD RETURN 276 ROWS FOR THE TECHNOLOGY SECTOR
date_start = '2015-01-02'   # THE START DATE
date_end = '2015-12-31'     # THE END DATE


######################################################################
data = pd.DataFrame() # INIT EMPTY DATAFRAME OBJECT TO CONCAT FINAL OUTPUT


######################################################################
# CREATE CONNECTION TO THE DATABASE
cnx = mysql.connector.connect(user='vsc', password='blaster123',
                              host='127.0.0.1',
                              database='stock')

# CREATE A CURSORS TO THE DATABASE
cursor = cnx.cursor(buffered=True)

mycursor = cnx.cursor()

######################################################################
# BUILD S&P 500 INDEX DATAFRAME FOR BENCHMARK RATIO BASELINE
sp500_query = ("SELECT sp.date AS 'date', sp.PctChange AS 'PercentChange' FROM sp500 AS sp "
               "WHERE (sp.date BETWEEN %s AND %s)")

# EXECUTE THE QUERY; GRAB THE RESULTS INTO sp500_result
cursor.execute(sp500_query, (date_start, date_end))
sp500_result = cursor.fetchall()


######################################################################
# BUILD A QUERY TO THE DATABASE FOR SECURITIES 
# TO INCLUDE IN THE DEA BENCHMARK ANALYSIS STUDY SET:
# ("SELECT DISTINCT Sector FROM stock.securities;")
# SECTORS AVAILABLE FOR USE (ex: sector='Technology'):
#       'Technology', 'Basic Materials', 'Consumer Discretionary',
#       'Consumer Staples', 'Energy', 'Finance', 'Health Care',
#       'Industrials', 'Real Estate', Telecommunications', 
#       'Utilities'
symbol_query = ("SELECT Symbol FROM securities "
         "WHERE sector='Utilities' ORDER BY Symbol ASC")

cursor.execute(symbol_query)

my_symbol_result = cursor.fetchall()

# LOOP THRU EACH SYMBOL RETURNED IN symbol_query SQL
for x in my_symbol_result:

    # SELECT ALL PRICE DATA WITHIN DATE RANGE FOR EACH SYMBOL
    query = ("SELECT p.date AS 'date', p.Symbol AS 'symbol', p.open AS 'open', p.close AS 'close', (((p.open-p.close)/p.close)*100) AS 'pct_change', sp.PctChange  FROM price_quotes AS p, sp500 AS sp "
             "WHERE p.Symbol=%s AND p.date = sp.date AND (p.date BETWEEN %s AND %s) AND (sp.date BETWEEN %s AND %s)")
    
    query_roi_start = ("SELECT p.date AS 'date', p.Symbol AS 'symbol', p.close AS 'close' FROM price_quotes AS p "
             "WHERE p.Symbol=%s AND (p.date = %s)")
    
    query_roi_end = ("SELECT p.date AS 'date', p.Symbol AS 'symbol', p.close AS 'close' FROM price_quotes AS p "
             "WHERE p.Symbol=%s AND (p.date = %s)")

    current_symbol = x[0] # THE CURRENT SYMBOL TEXT - FOR CODE READABILITY

    # EXECUTE THE QUERY
    cursor.execute(query, (current_symbol, date_start, date_end, date_start, date_end))

    # GET ALL THE RESULTS
    myresult = cursor.fetchall()

    # PLACE THE MYSQL OUTPUT RESULT LIST INTO A DATAFRAME OBJECT
    df = pd.DataFrame(myresult)

    # GET THE BEGINNING OF THE TIMEFRAME CLOSING PRICE
    cursor.execute(query_roi_start, (current_symbol, date_start))
    myresult_roi_start = cursor.fetchall()
    df_start = pd.DataFrame(myresult_roi_start)

    # GET THE ENDING OF THE TIMEFRAME CLOSING PRICE
    cursor.execute(query_roi_end, (current_symbol, date_end))
    myresult_roi_end = cursor.fetchall()
    df_end = pd.DataFrame(myresult_roi_end)

    #row_count = df.shape[0]
    #col_count = df.shape[1]

    # DROP EMPTY VALUE ROWS
    df.dropna(inplace=True)
    df_start.dropna(inplace=True)
    df_end.dropna(inplace=True)

    # IF DATA IS AVAILABLE FOR THE SYMBOL CALC BETA AND SIGMA VALUES FOR ENTIRE DATE RANGE
    if (not df.empty):
        # Create arrays for x and y variables in the regression model
        # Set up the model and define the type of regression
        x = np.array(df[4]).reshape((-1,1)) # STOCK SYMBOL PERCENT CHANGE
        y = np.array(df[5]) # S&P 500 MARKET PERCENT CHANGE
        model = LinearRegression().fit(x, y) # SOLVE THE MODEL

        print('Beta = ', model.coef_) # SLOPE = BETA
        df[6] = model.coef_[0]

        # CALCULATE THE SIGMA (STANDARD DEVIATION) OF PRICE % CHANGE
        df[7] = df[4].std() 

        # CALCULATE THE RATE OF RETURN FOR THE TIMEFRAME
        # Rate of Return % = [(Current Value – Initial Value) / Initial Value] x 100
        if (not df_start.empty and  not df_end.empty):
            rate_of_return = (((df_end[2] - df_start[2]) / df_start[2]) * 100)

        if (not rate_of_return.empty and not math.isnan(df[4].std())):
            sql = "INSERT INTO beta_sigma (symbol, date, beta, sigma, rate_of_return) VALUES (%s, %s, %s, %s, %s)"
            val = (current_symbol, date_end, model.coef_[0], df[4].std(), rate_of_return[0])
            mycursor.execute(sql, val)

            cnx.commit()
            print(mycursor.rowcount, "record inserted.")

            df[8] = rate_of_return[0]

            # CONCAT THE MYSQL DATAFRAME WITH THE FINAL OUTPUT DATAFRAME OBJECT
            data = pd.concat([data, df])

# ADD COL NAMES AFTER DATAFRAME HAS BEEN BUILT
data.columns = ['Date', 'Symbol', 'Open', 'Close', 'PricePctChange', 'SP500PctChg', 'Beta', 'Sigma', '1-YR-RateOfReturn']

print(data)

data.to_csv('pct_change_output.csv', index=False)

########################################################
# CLOSE THE DATABASE CONNECTION AND REFERENCE CURSOR
cursor.close()
mycursor.close()
cnx.close()