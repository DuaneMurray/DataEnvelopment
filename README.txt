11,306 TOTAL STOCK SYMBOLS SOURCED FROM TD AMERITRADE - FROM ALL SECTORS

Market Equity (size) = stock price * shares outstanding

Inputs:
Average Equity
average asset
sales costs

Outputs:
revenue
operating profit
net income

Momentum = Buy Volume / Sell Volume = BOS

an investment strategy with a long position of low-BOS winner stocks and a short position of high-BOS loser stocks can generate a higher return.

def O = open;
def H = high;
def C = close;
def L = low;
def V = volume;
def Buying = V*(C-L)/(H-L);
def Selling = V*(H-C)/(H-L);
BOSratio = Buying / Selling


Price to Earnings:


Price-to-Book Ratio:

High Book to Market ratio = value stock
long position in low book-to-market stocks and a short position
in high book-to-market stocks generates significantly abnormal returns

The market-to-book ratio, also called the price-to-book ratio, is the reverse of the book-to-market ratio. Like the book-to-market ratio, it seeks to evaluate whether a company's stock is over or undervalued by comparing the market price of all outstanding shares with the net assets of the company.

A market-to-book ratio above 1 means that the company’s stock is overvalued. A ratio below 1 indicates that it may be undervalued; the reverse is the case for the book-to-market ratio. Analysts can use either ratio to run a comparison on the book and market value of a firm.

ROA = Profitability-related fundamental

ALL NON-FINANCIAL FIRMS LISTED ON THE NYSE, AMEX, and NASDAQ:
1. Full return and price to book value data for the time frame
2. Exclude:
	A. Financial Firms
	B. Foreign Companies
	C. closed-end funds
	D. Real Estate Investment Trusts (REIT)
	E. American Depository Receipts (ADRs)
	F. Rirms with prices less than $5
	G. Firms with Negative Book-to-Market Values
3. Need:
	A. Returns
	B. Prices
	C. Trading Volume
	D. Financial Data

Low price-to-book ratio = value stocks <- WANT THIS
High price-to-book ratio = growth stocks


###################################################################
# ORIGINAL PROJECT README CONTENTS
###################################################################

DATA SOURCE PROCESS: [THE TECHNOLGY SECTOR HAS BEEN IMPORTED FOR THIS PROJECT]

0. Used NASDAQ online services to obtains lists of stock symbols for each Sector
    A. https://www.nasdaq.com/market-activity/stocks/screener

1. Used GOOGLEFINANCE API to obtain S&P 500 data (2012-July2023)
    A. =INDEXDATA("SPX","all","1/1/2012", "12/31/2023")

2. Used IEX service to obtain price history and fundamentals for NASDAQ Sector stocks
    A. Project/Data/IEX_Fundamentals_Import.py
    B. Project/Data/IEX_Price_History_Import.py
    C. Created CSV files containing the price and financial data from IEX

3. Imported the CSV files into MySQL Workbench to create tables (Table Data Import Wizard)
    A. Created Database: stock
    A. financials table
    B. price_quotes table
    C. securities table
    D. beta_sigma table
    D. sp500 table

4. Calculated Beta and Sigma values and placed into new database table
    A. Project/Data/fundamentals/beta_calculation.py for calculation and table insert
    B. MySQL beta_sigma table contains values for timeframe provided in the beta_calc script

5. Can update values for Beta, Sigma, investment date of portfolio, 1yr, 3yr, 5yr prices for rate of return calcs
    A. Project/Data/fundamentals/update_beta_calculations.py


DATA USAGE:

Sigma and Beta were calculated for the year end of 2015 (2015-12-31).
Initial backtesting investment date will be January 4, 2016 (2016-01-04)
    First trading day of the year after new years day holiday

Rate of Return % = [(Current Value – Initial Value) / Initial Value] x 100

One year return: 2016-12-31
Three year return: 2018-12-31
Five year return: 2020-12-31

DATES FOR RETURNS ANALYSIS:

Symbol  Date            Close
AMD	    2020-12-31	    91.71
AMD	    2019-12-31	    45.86
AMD	    2018-12-31	    18.46
AMD	    2017-12-29	    10.28
AMD	    2016-12-30	    11.34
AMD	    2015-12-30	    2.87

Get the investment amount:

=INDEX(GOOGLEFINANCE($A$3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2)

Get the close amount for specific future return date:

5 YR:
=((INDEX(GOOGLEFINANCE(H3, "close", DATE(2020,12,31), 1, "DAILY"), 2, 2) 
- INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2)) 
/ INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2))

3 YR:
=((INDEX(GOOGLEFINANCE(H3, "close", DATE(2018,12,31), 1, "DAILY"), 2, 2) 
- INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2)) 
/ INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2))

1 YR:
=((INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,12,30), 1, "DAILY"), 2, 2) 
- INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2)) 
/ INDEX(GOOGLEFINANCE(H3, "close", DATE(2016,1,4), 1, "DAILY"), 2, 2))


**NOTE ON DATA: DO NOT USE UNDERSCORES IN THE COLUMN NAMES - RMARKDOWN ERRORS OCCUR

DEA MODEL INPUTS:

SELECT DISTINCT p.symbol, b.beta, b.sigma, f.debtToEquity, f.pToBv
FROM price_quotes p, financials f, beta_sigma b
WHERE p.Symbol = b.Symbol AND p.Symbol = f.Symbol
AND p.date > '2014-12-31' AND p.date < '2016-01-01'
AND f.fiscalYear=2015;

DEA MODEL OUTPUTS:

SELECT DISTINCT f.symbol as 'DMU', f.netIncomeToRevenue AS 'O-NetMargin', 
f.incomeNetPerWabso AS 'O-EPS', f.returnOnAssets AS 'O-ReturnOnAssets', 
f.returnOnEquity as 'O-ReturnOnEquity', b.rate_of_return as 'O-1-YR-RateOfReturn'
FROM financials f, beta_sigma b
WHERE (f.symbol = b.symbol) AND f.fiscalYear=2015;

BOTH INPUTS AND OUTPUTS IN ONE FILE:

SELECT DISTINCT p.symbol AS 'DMU',
b.beta AS 'Beta', b.sigma AS 'Sigma', f.debtToEquity AS 'DToE', 
f.pToBv AS 'PToB', f.netIncomeToRevenue AS 'NetMrgn', 
f.incomeNetPerWabso AS 'EPS', f.returnOnAssets AS 'ROA', 
f.returnOnEquity as 'ROE', b.rate_of_return as 'TTMreturn',
b.investment_entry_price AS 'entryPrice', b.one_year_price AS 'oneYRprice', b.three_year_price AS 'threeYRprice',
b.five_year_price AS 'fiveYRprice', Sector as 'Sector'
FROM price_quotes p, financials f, beta_sigma b, securities s
WHERE p.Symbol = b.Symbol AND p.Symbol = f.Symbol AND p.symbol = s.Symbol
AND p.date > '2014-12-31' AND p.date < '2016-01-01'
AND f.fiscalYear='2015'
AND b.one_year_price IS NOT NULL
AND b.three_year_price IS NOT NULL
AND b.five_year_price IS NOT NULL
AND f.returnOnEquity IS NOT NULL
AND f.debtToEquity != 0
AND s.Sector = 'Technology';

/* 
SECTORS AVAILABLE FOR USE (ex: sector='Technology'):
      'Technology', 'Basic Materials', 'Consumer Discretionary',
       'Consumer Staples', 'Energy', 'Finance', 'Health Care',
       'Industrials', 'Real Estate', Telecommunications', 
       'Utilities'
*/


FINANCIAL MODELING PREP - DATA SOURCE FEED

REST API END POINTS (JSON):

COMPANY OUTLOOK
Provides all financial data

https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL


COMPANY PROFILE
A summary of important company information, including price, beta, market capitalization,description, headquarters, sector, industry, and more

https://financialmodelingprep.com/api/v3/profile/AAPL


DAILY CHART - HISTORICAL PRICES

symbol=string
from=date	2023-10-11
to=date		2023-01-09
https://financialmodelingprep.com/api/v3/historical-price-full/AAPL


RATIOS

symbol=string
period=annual, quarter
limit=number

https://financialmodelingprep.com/api/v3/ratios/AAPL?period=quarter


ECONOMIC INDICATORS

name=string	GDP, Real GDP, Unemployment rate, more...
from=date	2019-10-10
to=date		2021-11-10

https://financialmodelingprep.com/api/v4/economic?name=GDP


SECTOR PERFORMANCE

Current:
https://financialmodelingprep.com/api/v3/sector-performance

Historical:
https://financialmodelingprep.com/api/v3/historical-sectors-performance


ENVIRONMENTAL SOCIAL GOVERNANCE
environmental, social, governance scores

year=int	2022

https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-sector-benchmark?year=2022
