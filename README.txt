DATA SOURCE: FINANCIAL MODELING PREP (https://site.financialmodelingprep.com/)
REST API DOCS: https://site.financialmodelingprep.com/developer/docs

8,676 US STOCK SYMBOLS SOURCED WHERE ALL ROWS CONTAIN COMPLETE FINANCIAL AND TECHNICAL DATA

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

162 INDUSTRIES:
Advertising Agencies
Aerospace & Defense
Agricultural Inputs
Airlines
Airports & Air Services
Aluminum
Apparel Manufacturing
Apparel Retail
Application Software
Asset Management
Auto & Truck Dealerships
Auto Manufacturers
Auto Parts
Banks
Banks—Diversified
Banks—Regional
Beverages—Brewers
Beverages—Non-Alcoholic
Beverages—Wineries & Distilleries
Biotechnology
Broadcasting
Building Materials
Building Materials Wholesale
Building Products & Equipment
Business Equipment & Supplies
Business Services
Capital Markets
CATV Systems
Chemicals
Closed-End Fund - Equity
Coking Coal
Communication Equipment
Communication Services
Computer Hardware
Confectioners
Conglomerates
Consulting Services
Consumer Electronics
Copper
Credit Services
Department Stores
Diagnostics & Research
Discount Stores
Diversified Communication Services
Drug Manufacturers—General
Drug Manufacturers—Specialty & Generic
Education & Training Services
Electrical Equipment & Parts
Electronic Components
Electronic Gaming & Multimedia
Electronics & Computer Distribution
Engineering & Construction
Entertainment
Farm & Heavy Construction Machinery
Farm Products
Financial Conglomerates
Financial Data & Stock Exchanges
Food Distribution
Footwear & Accessories
Furnishings, Fixtures & Appliances
Gambling
Gold
Grocery Stores
Health Information Services
Healthcare Plans
Home Improvement Retail
Homebuilding & Construction
Household & Personal Products
Independent Oil & Gas
Industrial Distribution
Industrial Metals & Minerals
Information Technology Services
Infrastructure Operations
Insurance Brokers
Insurance Specialty
Insurance—Diversified
Insurance—Life
Insurance—Property & Casualty
Insurance—Reinsurance
Insurance—Specialty
Integrated Freight & Logistics
Internet Content & Information
Internet Retail
Leisure
Lodging
Lumber & Wood Production
Luxury Goods
Marine Shipping
Marketing Services
Medical Care Facilities
Medical Devices
Medical Distribution
Medical Instruments & Supplies
Metal Fabrication
Mortgage Finance
Oil & Gas Drilling
Oil & Gas E&P
Oil & Gas Equipment & Services
Oil & Gas Integrated
Oil & Gas Midstream
Oil & Gas Refining & Marketing
Other Industrial Metals & Mining
Other Precious Metals & Mining
Packaged Foods
Packaging & Containers
Paper & Paper Products
Personal Services
Pharmaceutical Retailers
Pollution & Treatment Controls
Publishing
Railroads
Real Estate Services
Real Estate—Development
Real Estate—Diversified
Recreational Vehicles
REIT—Diversified
REIT—Healthcare Facilities
REIT—Hotel & Motel
REIT—Industrial
REIT—Mortgage
REIT—Office
REIT—Residential
REIT—Retail
REIT—Specialty
Rental & Leasing Services
Residential Construction
Resorts & Casinos
Restaurants
Retail Apparel & Specialty
Scientific & Technical Instruments
Security & Protection Services
Semiconductor Equipment & Materials
Semiconductors
Shell Companies
Silver
Software—Application
Software—Infrastructure
Solar
Specialty Business Services
Specialty Chemicals
Specialty Industrial Machinery
Specialty Retail
Staffing & Employment Services
Steel
Telecom Services
Telecom Services - Foreign
Textile Manufacturing
Thermal Coal
Tobacco
Tools & Accessories
Travel Services
Trucking
Uranium
Utilities Diversified
Utilities Regulated
Utilities—Diversified
Utilities—Independent Power Producers
Utilities—Regulated Electric
Utilities—Regulated Gas
Utilities—Regulated Water
Utilities—Renewable
Waste Management


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


4. Calculated Beta and Sigma values and placed into new database table
    A. Project/beta_calculation.py for calculation and table insert
    B. MySQL beta_sigma table contains values for timeframe provided in the beta_calc script

5. Can update values for Beta, Sigma, investment date of portfolio, 1yr, 3yr, 5yr prices for rate of return calcs
    A. Project/update_beta_calculations.py


DATA USAGE:

Rate of Return % = [(Current Value – Initial Value) / Initial Value] x 100


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

