#load libraries
import yfinance as yf
from yahoofinancials import YahooFinancials
import numpy as np
from sklearn.linear_model import LinearRegression


dhr = yf.Ticker('DHR')

info = dhr.info
#data = dhr.history()
data = dhr.history(interval='1d', start='2000-01-03', end='2023-09-01')

data.head()
info.keys()

