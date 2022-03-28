import pandas as pd
import numpy as np
import plotly.express as px


prices = pd.read_csv('data/gas_price_US.csv',
                engine = 'python',
                parse_dates = True)

pollution = pd.read_csv('data/pollution_2000_2021.csv',
                engine = 'python',
                parse_dates = True)
del pollution["Year"]
del pollution["Month"]
del pollution["Day"]

prices['Date'] = pd.to_datetime(prices['Date'], format='%m/%d/%Y')
prices = prices.loc[(prices['Date'] >= '2000-01-03')]

fig = px.line(prices, x="Date", y="Regular All Formulations Retail Gasoline Prices Dollars per Gallon", title='Gas price per week')
fig.show()

