# LOAD LIBRARIES
import math
import mysql.connector
from sqlalchemy import create_engine
#import datetime
import yfinance as yf
from yahoofinancials import YahooFinancials
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

######################################################################
data = pd.DataFrame() # INIT EMPTY DATAFRAME OBJECT TO CONCAT FINAL OUTPUT
symbol_list = "" # CREATE EMPTY STRING VAR
fundamental_valuations = pd.DataFrame() # CREATE EMPTY DATAFRAME

######################################################################
# LOAD LIST OF STOCKS TO INSERT INTO THE DATABASE
stock_list = pd.read_csv("Data/Symbols-TEST.csv") # TESTING DATA FILE

#stock_list = pd.read_csv("Data/Symbols-Communications-Services.csv")
#stock_list = pd.read_csv("Data/Symbols-Consumer-Discretionary.csv")
#stock_list = pd.read_csv("Data/Symbols-Consumer-Staples.csv")
#stock_list = pd.read_csv("Data/Symbols-Energy.csv")
#stock_list = pd.read_csv("Data/Symbols-Financials.csv")
#stock_list = pd.read_csv("Data/Symbols-Health-Care.csv")
#stock_list = pd.read_csv("Data/Symbols-Industrials.csv")
#stock_list = pd.read_csv("Data/Symbols-Information-Technology.csv")
#stock_list = pd.read_csv("Data/Symbols-Materials.csv")
#stock_list = pd.read_csv("Data/Symbols-Real-Estate.csv")
#stock_list = pd.read_csv("Data/Symbols-Utilities.csv")

######################################################################
# CREATE CONNECTION TO THE DATABASE
cnx = mysql.connector.connect(user='vsc', password='blaster123',
                              host='127.0.0.1',
                              database='stockdata')

# CREATE A CURSORS TO THE DATABASE
cursor = cnx.cursor(buffered=True) 
mycursor = cnx.cursor()

# USER, PW, AND DB ARE BEING IMPORTED FROM dbconfig.py FILE
db_data = ("mysql+mysqlconnector://{user}:{pw}@localhost/{db}"
           .format(user = "vsc",
                   pw = "blaster123",
                   db = "stockdata"))

engine = create_engine(db_data).connect()

# import important module
import datetime
from datetime import datetime

for x in stock_list['Symbol']:
    # GET FUNDAMENTALS HISTORY
    #yahoo_financials = YahooFinancials(x)
    fundamentals = yf.Ticker(x)
    fundamental_val = pd.DataFrame(fundamentals.info)
    #(pd.to_timedelta(fundamental_val['governanceEpochDate'], unit='s') + pd.to_datetime('1960-1-1'))
    #fundamental_val.keys()
    
    # Create datetime string
    #datetime_str = fundamental_val['governanceEpochDate']
    #print("datetime string : {}".format(datetime_str))
    
    # call datetime.strptime to convert
    # it into datetime datatype
    #datetime_obj = datetime.strptime(datetime_str,
    #                                "%d%m%y%H%M%S")
    
    fundamental_val['governanceEpochDate'] = pd.to_datetime(fundamental_val['governanceEpochDate'], unit='s')
    fundamental_val['compensationAsOfEpochDate'] = pd.to_datetime(fundamental_val['compensationAsOfEpochDate'], unit='s')
    fundamental_val['exDividendDate'] = pd.to_datetime(fundamental_val['exDividendDate'], unit='s')
    fundamental_val['lastFiscalYearEnd'] = pd.to_datetime(fundamental_val['lastFiscalYearEnd'], unit='s')
    fundamental_val['nextFiscalYearEnd'] = pd.to_datetime(fundamental_val['nextFiscalYearEnd'], unit='s')
    fundamental_val['mostRecentQuarter'] = pd.to_datetime(fundamental_val['mostRecentQuarter'], unit='s')
    fundamental_val['lastSplitDate'] = pd.to_datetime(fundamental_val['lastSplitDate'], unit='s')
    fundamental_val['lastDividendDate'] = pd.to_datetime(fundamental_val['lastDividendDate'], unit='s')
    fundamental_val['firstTradeDateEpochUtc'] = pd.to_datetime(fundamental_val['firstTradeDateEpochUtc'], unit='s')
    fundamental_val['dateShortInterest'] = pd.to_datetime(fundamental_val['dateShortInterest'], unit='s')

# `governanceEpochDate`, `compensationAsOfEpochDate`,
# `exDividendDate`, `lastFiscalYearEnd`, `nextFiscalYearEnd`,
# `mostRecentQuarter`, `lastSplitDate`, `lastDividendDate`,
# `firstTradeDateEpochUtc`

    # It will print the datetime object
    #print(datetime_obj)
    #print(new_date)
    
    # extract the time from datetime_obj
    #date = datetime_obj.date()
    
    # it will print date that we have
    # extracted from datetime obj
    #print(date)






    # ANNUAL FINANCIALS
    pnl = fundamentals.financials
    bs = fundamentals.balancesheet
    cf = fundamentals.cashflow
    fs = pd.concat([pnl,bs,cf])

    a_temp_fs = fs.T
    a_temp_fs['Symbol'] = x
    a_temp_fs.index.name = 'Date'

    #a_temp_fs.to_csv('annual_new.csv')
    a_temp_fs.to_sql(name='a_financials', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE

    # QUARTERLY FINANCIALS
    q_pnl = fundamentals.quarterly_financials
    q_bs = fundamentals.quarterly_balancesheet
    q_cf = fundamentals.quarterly_cash_flow
    q_fs = pd.concat([q_pnl,q_bs,q_cf])

    q_temp_fs = q_fs.T
    q_temp_fs['Symbol'] = x
    q_temp_fs.index.name = 'Date'

    #q_temp_fs.to_csv('quarterly.csv')
    q_temp_fs.to_sql(name='q_financials', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE

    # SLICE THE DATAFRAME, KEEP HEADER ROW, KEEP ONE ROW OF VALUES
    fundamental_val = fundamental_val.iloc[1:2,:]
    fundamental_val.drop(columns=['companyOfficers'], inplace=True)
    fundamental_val.to_sql(name='fundamentals', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE




    symbol = fundamental_val['symbol']

    # INPUTS
    debt_to_equity = fundamental_val['debtToEquity']
    price_to_book = fundamental_val['priceToBook']
    beta = fundamental_val['beta']
    sigma = 0 # STD DEVIATION

    # OUTPUTS
    tralingEPS = fundamental_val['trailingEps']
    forwardEPS = fundamental_val['forwardEps']
    ROA = fundamental_val['returnOnAssets']
    ROE = fundamental_val['returnOnEquity']
    profit_margin = fundamental_val['profitMargins']
    ebita_margin = fundamental_val['ebitdaMargins']


    ft_employees = fundamental_val['fullTimeEmployees']
    dividend_rate = fundamental_val['dividendRate']
    dividend_yield = fundamental_val['dividendYield']
    trailingPE = fundamental_val['trailingPE']
    forwardPE = fundamental_val['forwardPE']
    shares_outstanding = fundamental_val['sharesOutstanding']
    book_value = fundamental_val['bookValue']
    PEG_ratio = fundamental_val['pegRatio']
    traling_PEG = fundamental_val['trailingPegRatio']
    target_high = fundamental_val['targetHighPrice']
    target_low = fundamental_val['targetLowPrice']
    analyst_coverage = fundamental_val['numberOfAnalystOpinions']
    earnings_bitda = fundamental_val['ebitda']
    quick_ratio = fundamental_val['quickRatio']
    current_ratio = fundamental_val['currentRatio']
    total_revenue = fundamental_val['totalRevenue']
    revenue_per_share = fundamental_val['revenuePerShare']
    gross_margin = fundamental_val['grossMargins']
    operating_margin = fundamental_val['operatingMargins']
    
    #fundamental_valuations['date'] = pd.to_datetime(fundamental_valuations['date']/1000, unit="s")
    #fundamental_valuations['date'] = pd.to_datetime(fundamental_valuations['date'], unit="s")
    f_filename = x + '-Fundamentals.csv'
    fundamental_val.to_csv('Data/Fundamentals/' + f_filename, index=False)

    # GET PRICE HISTORY
    price_val = fundamentals.history() # GET ALL PRICE DATA FOR SYMBOL FROM YFINANCE
    price_val['symbol'] = x
    #price_val['Date'] = pd.to_datetime(price_val['Date']/1000, unit="s")
    price_val.to_sql(name='prices', con=engine, chunksize=430, if_exists='append') # ADD DATA TO EXISTING TABLE

    p_filename = x + '-Price-History.csv'
    price_val.to_csv('Data/Prices/' + p_filename, index=True)
