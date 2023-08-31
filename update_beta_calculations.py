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

investment_date = '2016-01-04' # END OF YEAR CLOSE
one_year_date = '2016-12-30'
three_year_date = '2018-12-31'
five_year_date = '2020-12-31'


#SELECT date, close FROM stock.price_quotes 
#WHERE symbol = 'AMD' 
#AND 
#(
#date = '2020-12-31' 
#OR date = '2019-12-31'
#OR date = '2018-12-31'
#OR date = '2017-12-29'
#OR date = '2016-01-04' /* INVESTMENT DATE */
#OR date = '2016-12-30'
#OR date = '2015-12-30'
#)
#order by date DESC;


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
    # GET ALL THE RESULTING DATA
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

    # DROP EMPTY VALUE ROWS
    df.dropna(inplace=True)
    df_start.dropna(inplace=True)
    df_end.dropna(inplace=True)

    # GET THE CLOSE PRICES FOR EACH FUTURE RETURNS CALCULATION FOR BACKTESTING
    query_investment_date = "SELECT close FROM stock.price_quotes WHERE symbol=%s AND date=%s"
    cursor.execute(query_investment_date, (current_symbol, investment_date))
    investment_date_result = cursor.fetchall()
    df_investment_return = pd.DataFrame(investment_date_result)

    query_one_year_date = "SELECT close FROM stock.price_quotes WHERE symbol=%s AND date=%s"
    cursor.execute(query_investment_date, (current_symbol, one_year_date))
    one_year_date_result = cursor.fetchall()
    df_one_year_return = pd.DataFrame(one_year_date_result)

    query_three_year_date = "SELECT close FROM stock.price_quotes WHERE symbol=%s AND date=%s"
    cursor.execute(query_investment_date, (current_symbol, three_year_date))
    three_year_date_result = cursor.fetchall()
    df_three_year_return = pd.DataFrame(three_year_date_result)

    query_five_year_date = "SELECT close FROM stock.price_quotes WHERE symbol=%s AND date=%s"
    cursor.execute(query_investment_date, (current_symbol, five_year_date))
    five_date_result = cursor.fetchall()
    df_five_year_return = pd.DataFrame(five_date_result)

    # IF DATA IS AVAILABLE FOR THE SYMBOL CALC BETA AND SIGMA VALUES FOR ENTIRE DATE RANGE
    if (not df.empty and not df_investment_return.empty and not df_one_year_return.empty and not df_three_year_return.empty
        and not df_five_year_return.empty):
        # Create arrays for x and y variables in the regression model
        # Set up the model and define the type of regression
        x = np.array(df[4]).reshape((-1,1)) # STOCK SYMBOL PERCENT CHANGE
        y = np.array(df[5]) # S&P 500 MARKET PERCENT CHANGE
        model = LinearRegression().fit(x, y) # SOLVE THE MODEL

        #print('Beta = ', model.coef_) # SLOPE = BETA
        df[6] = model.coef_[0]

        # CALCULATE THE SIGMA (STANDARD DEVIATION) OF PRICE % CHANGE
        df[7] = df[4].std() 

        # CALCULATE THE RATE OF RETURN FOR THE TIMEFRAME
        # Rate of Return % = [(Current Value – Initial Value) / Initial Value] x 100
        if (not df_start.empty and  not df_end.empty):
            rate_of_return = (((df_end[2] - df_start[2]) / df_start[2]) * 100)

        #
        #
        # CHANGE BELOW TO AN UPDATE SQL COMMAND
        #
        if (not rate_of_return.empty and not math.isnan(df[4].std())):
            entry_price = df_investment_return._get_value(0,0,takeable = True)
            one_year_price = df_one_year_return._get_value(0,0,takeable = True)
            three_year_price = df_three_year_return._get_value(0,0,takeable = True)
            five_year_price = df_five_year_return._get_value(0,0,takeable = True)

            #sql = "INSERT INTO beta_sigma (symbol, date, beta, sigma, rate_of_return) VALUES (%s, %s, %s, %s, %s)"
            #val = (current_symbol, date_end, model.coef_[0], df[4].std(), rate_of_return[0])
            #mycursor.execute(sql, val)
            
            sql = "UPDATE beta_sigma SET date=%s, beta=%s, sigma=%s, rate_of_return=%s, investment_entry_price=%s, one_year_price=%s, three_year_price=%s, five_year_price=%s WHERE symbol=%s"
            cursor.execute(sql, (date_end, model.coef_[0], df[4].std(), rate_of_return[0], entry_price, one_year_price, three_year_price, five_year_price, current_symbol))

            cnx.commit()
            #print(mycursor.rowcount, "record inserted.")

            df[8] = rate_of_return[0]

            #DataFrame._get_value(index, col, takeable=False) 
            df[9] = df_investment_return._get_value(0,0,takeable = True)
            df[10] = df_one_year_return._get_value(0,0,takeable = True)
            df[11] = df_three_year_return._get_value(0,0,takeable = True)
            df[12] = df_five_year_return._get_value(0,0,takeable = True)

            print(df)

            # CONCAT THE MYSQL DATAFRAME WITH THE FINAL OUTPUT DATAFRAME OBJECT
            data = pd.concat([data, df])

# ADD COL NAMES AFTER DATAFRAME HAS BEEN BUILT
data.columns = ['Date', 'Symbol', 'Open', 'Close', 'PricePctChange', 'SP500PctChg', 'Beta', 'Sigma', 'TTMrateOfReturn', 'buyPrice', 'oneYRprice', 'threeYRprice', 'fiveYRprice']

print(data)

data.to_csv('pct_change_output.csv', index=False)

########################################################
# CLOSE THE DATABASE CONNECTION AND REFERENCE CURSOR
cursor.close()
mycursor.close()
cnx.close()