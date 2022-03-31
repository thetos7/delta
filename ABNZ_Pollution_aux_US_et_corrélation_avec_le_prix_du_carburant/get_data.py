import pandas as pd
import numpy as np
import glob
import plotly.express as px

# Pollution data
# --------------------------------------------------------------------------------------

pollution = pd.read_csv('data/pollution_2000_2021.csv',
                engine = 'python',
                parse_dates = True)
del pollution["Year"]
del pollution["Month"]
del pollution["Day"]
del pollution["Address"]
del pollution["County"]
del pollution["City"]
del pollution["O3 1st Max Value"]
del pollution["O3 1st Max Hour"]
del pollution["O3 AQI"]
del pollution["CO 1st Max Value"]
del pollution["CO 1st Max Hour"]
del pollution["CO AQI"]
del pollution["SO2 1st Max Value"]
del pollution["SO2 1st Max Hour"]
del pollution["SO2 AQI"]
del pollution["NO2 1st Max Value"]
del pollution["NO2 1st Max Hour"]
del pollution["NO2 AQI"]

# converting string dates to dates types
pollution['Date'] = pd.to_datetime(pollution['Date'], format='%Y-%m-%d')

# sort data by date
pollution = pollution.sort_values(["Date"])

# getting the mean of values at each date, ignoring the states where the data was taken from
pollution = pollution.resample('d', on='Date').mean()

# drawing graphs
O3fig = px.line(pollution, y="O3 Mean", title='O3 per day')
COfig = px.line(pollution, y="CO Mean", title='CO per day')
SO2fig = px.line(pollution, y="SO2 Mean", title='SO2 per day')
NO2fig = px.line(pollution, y="NO2 Mean", title='NO2 per day')
O3fig.show()
COfig.show()
SO2fig.show()
NO2fig.show()

# Prices data
# --------------------------------------------------------------------------------------

prices = pd.read_csv('data/gas_price_US.csv',
                engine = 'python',
                parse_dates = True)

# converting string dates to dates types
prices['Date'] = pd.to_datetime(prices['Date'], format='%m/%d/%Y')

# removing dates too old
prices = prices.loc[(prices['Date'] >= '2000-01-03')]

# drawing graph
pricesFig = px.line(prices, x="Date", y="Regular All Formulations Retail Gasoline Prices Dollars per Gallon", title='Gas price per week')
pricesFig.show()

# Temperature and precipitation data
# --------------------------------------------------------------------------------------

path = 'data/US_weather_data/'
filenames = glob.glob(path + "/*.csv")
cities = []

for f in filenames:
    df = pd.read_csv(f, engine = 'python', parse_dates = True)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df.loc[(df['Date'] >= '2000-01-03')]
    df['average_celsius'] = (df[['tmax', 'tmin']].mean(axis=1) - 32)/1.8
    df['prcp'] = df['prcp']/2.54
    df.rename(columns={'prcp': 'prcp_cm'}, inplace=True)
    del df['tmax']
    del df['tmin']
    df = df.iloc[: , 1:]
    cities.append(df)

# averaging all cities data
average_cities = pd.concat(cities).groupby('Date', as_index=False).mean()

# drawing graphs
celsiusFig = px.line(average_cities, x="Date", y="average_celsius", title='average_celsius')
prcpFig = px.line(average_cities, x="Date", y="prcp_cm", title='prcp_cm')
celsiusFig.show()
prcpFig.show()
