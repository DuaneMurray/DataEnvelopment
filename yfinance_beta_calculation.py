#load libraries
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

# symbols = [stock, market]
# start date for historical prices
symbols = ['AXP', 'SPY']
data = yf.download(symbols, '2020-2-22', '2021-2-22')['Adj Close']

# Convert historical stock prices to daily percent change
price_change = data.pct_change()

# Deletes row one containing the NaN
df = price_change.drop(price_change.index[0])

# Create arrays for x and y variables in the regression model
# Set up the model and define the type of regression
x = np.array(df['AXP']).reshape((-1,1))
y = np.array(df['SPY'])
model = LinearRegression().fit(x, y)

print('Beta = ', model.coef_) # SLOPE = BETA