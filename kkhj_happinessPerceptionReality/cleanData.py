#calculate number of countries for each value for each year  --> 1
#create plot wit that value + gid for each year              --> 1

# calculate entire area for each year                       --> 1 TUE
#calculate each are for each country per year               --> 1 WED
#add column with area/toal * 10                             --> 1 WED


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_gdp_values():
    df = pd.read_csv("data/PIB.csv")
    df['GDP'] = df['Value']/10000
    df['GDP'] = df['GDP'].astype(int)
    min_year = 2012
    max_year = 2021

    for  i in range (min_year, max_year+1):
        year_df = df[df['TIME'] == i]
        yearly_gdp = pd.Series(year_df['Value'])
        yearly_gdp.plot.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
    plt.show()




    #for range in year
    #for range in gpd
    #count number of countries
    #represent hist where x is gdp level and y is number of countries

#def get_nbr_countries_year():


get_gdp_values()


"""
# Generate data on commute times.
size, scale = 1000, 10
commutes = pd.Series(np.random.gamma(scale, size=size) ** 1.5)
print(commutes)
commutes.plot.hist(grid=True, bins=20, rwidth=0.9,color='#607c8e')
plt.title('Commute Times for 1,000 Commuters')
plt.xlabel('Counts')
plt.ylabel('Commute Time')
plt.grid(axis='y', alpha=0.75)
#plt.show()"""

