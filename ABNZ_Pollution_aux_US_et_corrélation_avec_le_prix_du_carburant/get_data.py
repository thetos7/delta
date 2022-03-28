import pandas as pd
import numpy as np


prices = pd.read_csv('data/gas_price_US.csv',
                engine = 'python',
                parse_dates = True)

#pollution = pd.read_csv('data/pollution_2000_2021.csv',
#                engine = 'python',
#                parse_dates = True)

prices['Date'] = pd.to_datetime(prices['Date'], format='%m/%d/%Y')
prices = prices.loc[(prices['Date'] >= '2020-01-03')]

print(prices)
