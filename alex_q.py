import numpy as np

import pandas as pd

import datetime as dt

import matplotlib.pyplot as plt

from scipy.optimize import minimize #, rosen, rosen_der

 

#Pulls in monthly and weekly DOW30 stock prices back to 2000 from CSV files, drops columns with incomplete price history

 

data_weekly = pd.read_csv('data/data_weekly.csv')

data_weekly.drop(['V', 'DOW'], axis=1, inplace=True)

data_weekly.Date = pd.to_datetime(data_weekly.Date)

data_weekly.set_index('Date', inplace=True)

 

data_monthly = pd.read_csv('data/data_monthly.csv')

data_monthly.drop(['V', 'DOW'], axis=1, inplace=True)

data_monthly.Date = pd.to_datetime(data_monthly.Date)

data_monthly.set_index('Date', inplace=True)

 

log_weekly = np.log(data_weekly/data_weekly.shift(1))

log_weekly = log_weekly.iloc[1:]

 

log_monthly = np.log(data_monthly/data_monthly.shift(1))

log_monthly = log_monthly.iloc[1:]

 
print(log_monthly)
 