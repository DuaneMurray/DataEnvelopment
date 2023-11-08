DATA SOURCE: FINANCIAL MODELING PREP (https://site.financialmodelingprep.com/)
REST API DOCS: https://site.financialmodelingprep.com/developer/docs

8,676 US TRADED STOCK SYMBOLS SOURCED WHERE ALL ROWS CONTAIN COMPLETE FINANCIAL AND TECHNICAL DATA
8,640 US TRADED STOCK SYMBOLS WITH COMPLETE FINANCIAL, TECHNICAL, AND PRICING DATA

ALL NON-FINANCIAL FIRMS LISTED ON THE NYSE, AMEX, and NASDAQ:
Exclude:
	A. Financial Firms - uses debt as an asset/receivable instead of a liability
	C. Closed-end funds
	D. Real Estate Investment Trusts (REIT)
	E. American Depository Receipts (ADRs)
	F. Warrants (W or -W at end of symbol)
	G. Firms with Negative Book-to-Market Values


REST API END POINTS (JSON):

COMPANY OUTLOOK
	
	Provides all financial data

	https://financialmodelingprep.com/api/v4/company-outlook?symbol=AAPL


COMPANY PROFILE
	
	A summary of important company information, including price, beta, market capitalization,description, headquarters, sector, industry, and more

	https://financialmodelingprep.com/api/v3/profile/AAPL


DAILY CHART - HISTORICAL PRICES

Params:
	symbol=string
	from=date	2023-10-11
	to=date		2023-01-09

	https://financialmodelingprep.com/api/v3/historical-price-full/AAPL


RATIOS

Params:
	symbol=string
	period=annual, quarter
	limit=number

	https://financialmodelingprep.com/api/v3/ratios/AAPL?period=quarter


ECONOMIC INDICATORS

Params:
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

Param: 
	year=int

	https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-sector-benchmark?year=2022


11 SECTORS:
Financial Services
Basic Materials
Consumer Defensive
Industrials
Energy
Healthcare
Communication Services
Consumer Cyclical
Technology
Real Estate
Utilities


INITIAL MODELING CONCEPTS:

Market Equity (size) = stock price * shares outstanding

Inputs:
Average Equity
Average asset
Sales costs

Outputs:
Revenue
Operating profit
Net income

BOS = Momentum = Buy Volume / Sell Volume

An investment strategy with a long position of low-BOS (winner stocks) and a short position 
of high-BOS (loser stocks) may potentially generate higher returns.

O = open;
H = high;
C = close;
L = low;
V = volume;
Buying = V*(C-L)/(H-L);
Selling = V*(H-C)/(H-L);
BOSratio = Buying / Selling


Price to Earnings:


Price-to-Book Ratio:

High Book to Market ratio = value stock
long position in low book-to-market stocks and a short position
in high book-to-market stocks generates significantly abnormal returns

The market-to-book ratio, also called the price-to-book ratio, is the reverse of the book-to-market ratio. Like the book-to-market ratio, it seeks to evaluate whether a company's stock is over or undervalued by comparing the market price of all outstanding shares with the net assets of the company.

A market-to-book ratio above 1 means that the company’s stock is overvalued. A ratio below 1 indicates that it may be undervalued; the reverse is the case for the book-to-market ratio. Analysts can use either ratio to run a comparison on the book and market value of a firm.

ROA = Profitability-related fundamental

Low price-to-book ratio = value stocks <- WANT THIS
High price-to-book ratio = growth stocks


DATA USAGE:

Rate of Return % = [(Current Value – Initial Value) / Initial Value] x 100

BETA:

The beta value is the rate of return for the stock divided by the rate of return of the comparision market
over the same returns holding period, or can be calculated using a regression method using the value of 
the slope coefficient for the predictor variable (x). Is scaled as a percentage:

	B = Stock Rate of Return / Market Rate of Return
	--OR--
	B = Slope = X coefficient from regression calculation

SIGMA (sd):

The sigma value is the standard deviation (sd) in price over a given time period. In this case,
the close price of a stock is used for the calculation over the same holding period used for
the beta calcuation.

DEA MODEL INPUTS:

SELECT DISTINCT p.symbol, b.beta, b.sigma, f.debtToEquity, f.pToBv
FROM price_quotes p, financials f, beta_sigma b
WHERE p.Symbol = b.Symbol AND p.Symbol = f.Symbol
AND p.date > '2014-12-31' AND p.date < '2016-01-01'
AND f.fiscalYear=2015;


SQL
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


