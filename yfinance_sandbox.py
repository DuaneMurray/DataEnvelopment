#load libraries
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression


dhr = yf.Ticker('DHR')

info = dhr.info
#data = dhr.history()
data = dhr.history(interval='1m', start='2022-01-03', end='2022-01-10')

data.head()
info.keys()
