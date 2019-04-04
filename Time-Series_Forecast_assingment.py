#import packages
import pandas as pd
from pandas import datetime
import numpy as np


#to plot within notebook
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
plt.style.use('fivethirtyeight')
# Above is a special style template for matplotlib, highly useful for visualizing time series data

import seaborn as sns
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 10,10

# lodind data using pandas library 

TCS = pd.read_csv('Data_tcs_stock.csv', parse_dates=['Date'])

INFY = pd.read_csv('Data_infy_stock.csv', parse_dates=['Date'])

NIFTY = pd.read_csv('Data_nifty_it_index.csv', parse_dates=['Date'])

#creating a data frame in one list
stocks = [TCS, INFY, NIFTY]


TCS.name = 'TCS'
INFY.name = 'INFY'
NIFTY.name = 'NIFTY_IT'
# this to_datetime method helps to convert string Date time into Python Date time object
TCS["Date"] = pd.to_datetime(TCS["Date"])
INFY["Date"] = pd.to_datetime(INFY["Date"])
NIFTY["Date"] = pd.to_datetime(NIFTY["Date"])

# data extraction

# the following added feature block appends new columns in data(TCS, INFY, NIFTY)

def features_build(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df.Date.dt.month
    df['Day'] = df.Date.dt.day
    df['WeekOfYear'] = df.Date.dt.weekofyear
    
for i in range(len(stocks)):
    features_build(stocks[i])

#we select Close as a target variable.
    
def moving_average(series, n):
    """
        Calculate average of last n observations
        
        n - rolling window
    """
    return np.average(series[-n:])

# next we are calculating a moving average(close price) for weeks
weeks = [4, 16, 28, 40, 52]
def indexing(stock):
    stock.index = stock['Date'] ## indexing the Datetime to get the time period on the x-axis. 
    
    return stock
indexing(TCS)
indexing(INFY)
indexing(NIFTY)
# First Resampling into Weeks format to calculate for weeks
# M.A using inbuilt function    
def plot_time_series(stock, weeks):
    
    dummy = pd.DataFrame()
    dummy['Close'] = stock['Close'].resample('W').mean() 
     
    for i in range(len(weeks)):
        m_a = dummy['Close'].rolling(weeks[i]).mean() 
        dummy[" Mov.AVG for " + str(weeks[i])+ " Weeks"] = m_a
        print('Calculated Moving Averages: for {0} weeks: \n\n {1}' .format(weeks[i], dummy['Close']))
    dummy.plot(title="Moving Averages for {} \n\n" .format(stock.name))    


plot_time_series(TCS)

plot_time_series(INFY)
plot_time_series(NIFTY)

# next we are using a window size = 10 then we use window size = 75


TCS = TCS.asfreq('D', method ='pad')       
INFY = INFY.asfreq('D', method ='pad')
NIFTY = NIFTY.asfreq('D', method ='pad')


TCS.name = 'TCS'
INFY.name = 'INFY'
NIFTY.name = 'NIFTY_IT'
#we create a rolling window of size 10 on each stock/index

window_size = [10, 75]
def plot_roll_win(stock):
    
    dummy = pd.DataFrame()
    
    dummy['Close'] = stock['Close']
     
    for i in range(len(window_size)):
        m_a = dummy['Close'].rolling(window_size[i]).mean() # M.A using predefined function
        dummy[" Mov.AVG for " + str(window_size[i])+ " Roll Window"] = m_a
        print('Calculated Moving Averages: for {0} weeks: \n\n {1}' .format(window_size[i], dummy['Close']))
    dummy.plot.line(title="Moving Averages for {} \n\n" .format(stock.name))

plot_roll_win(TCS)
plot_roll_win(INFY)
plot_roll_win(NIFTY)

#3.1 Volume shocks

def volume_shocks(stock):
    stock["vol_t+1"] = stock.Volume.shift(1)
    
    stock["volume_shock"] = ((abs(stock["vol_t+1"] - stock["Volume"])/stock["Volume"]*100)  > 10).astype(int)
    
    return stock
volume_shocks(TCS)
volume_shocks(INFY)
volume_shocks(NIFTY)
# considering only shock - 1 valued rows.
# 0 for negative and 1for positive
def direction_fun(stock):
    

    if stock["volume_shock"] == 0:
        pass
    else:
        if (stock["vol_t+1"] - stock["Volume"]) < 0:
            return 0
        else:
            return 1    
def vol_shock_direction(stock):
    stock['VOL_SHOCK_DIR'] = 'Nan'
    stock['VOL_SHOCK_DIR'] = stock.apply(direction_fun, axis=1)
    return stock


vol_shock_direction(TCS)
vol_shock_direction(INFY)
vol_shock_direction(NIFTY)

def price_shocks(stock):
    """
    'ClosePrice' - Close_t
    'Close Price next day - vol_t+1
    
    """
    stock["price_t+1"] = stock.Close.shift(1)  #next rows value
    
    stock["price_shock"] = (abs((stock["price_t+1"] - stock["Close"])/stock["Close"]*100)  > 2).astype(int)
    
    stock["price_black_swan"] = stock['price_shock'] # Since both had same data anad info/
    
    return stock
price_shocks(TCS)
price_shocks(INFY)
price_shocks(NIFTY)
def direction_fun_price(stock):
    
    # considerng only shock - 1 valued rows.
    # 0 - negative and 1- positive
    if stock["price_shock"] == 0:
        pass
    else:
        if (stock["price_t+1"] - stock["Close"]) < 0:
            return 0
        else:
            return 1
def price_shock_direction(stock):
    stock['PRICE_SHOCK_DIR'] = 'Nan'
    stock['PRICE_SHOCK_DIR'] = stock.apply(direction_fun_price, axis=1)
    return stock
vol_shock_direction(TCS)
vol_shock_direction(INFY)
vol_shock_direction(NIFTY)

def price_shock_wo_vol_shock(stock):
    
    stock["not_vol_shock"]  = (~(stock["volume_shock"].astype(bool))).astype(int)
    stock["price_shock_w/0_vol_shock"] = stock["not_vol_shock"] & stock["price_shock"]
    
    return stock


price_shock_wo_vol_shock(TCS)
price_shock_wo_vol_shock(INFY)
price_shock_wo_vol_shock(NIFTY)






