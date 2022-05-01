import pandas as pd
from pathlib import Path

from pandas import DataFrame


def clean_temperature_data():
    temp_country = pd.read_csv('bad_global_land_temperatures_by_country.csv')
    # Removing the duplicated countries and countries for which no information about the temperature
    temp_country_clean = DataFrame(temp_country[~temp_country['Country'].isin(
        ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands', 'United Kingdom', 'Africa', 'South America'])])
    temp_country_clean.replace(
        ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
        ['Denmark', 'France', 'Netherlands', 'United Kingdom'], inplace=True)
    temp_country_clean_copy = temp_country_clean.copy()
    temp_country_clean_copy['dt'] = pd.to_datetime(temp_country_clean['dt'])
    start_date = pd.to_datetime('1900-1-1')
    mask = temp_country_clean_copy['dt'] >= start_date
    temp_country_1900 = temp_country_clean_copy.loc[mask]
    temp_country_yearly = temp_country_1900.groupby([pd.Grouper(key='dt', freq='Y'), 'Country'])[
        'AverageTemperature'].mean().reset_index(name='Year')
    temp_country_yearly.rename(columns={'dt': 'Year', 'Year': 'AverageTemperature'}, inplace=True)
    temp_country_yearly['Year'] = pd.DatetimeIndex(temp_country_yearly['Year']).year
    filepath = Path('./clean/clean_global_land_temperature_by_country.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    temp_country_yearly.to_csv(filepath)


def clean_emission_data():
    emission = pd.read_csv('bad_historical_emission_by_country.csv')
    # Calculate and add Mean values of emission of each industrial sectors of each countries
    emission['Mean'] = emission.iloc[:, 5:34].mean(axis=1).round(decimals=3)
    # Get the total emission of all industrial sectors of each country
    total_emission = emission[emission['Sector'] == 'Total including LUCF']
    # Display by each year
    emission_countries_yearly = total_emission.melt(id_vars=["Country"], value_vars=total_emission.iloc[:, 5:34],
                                                    var_name="Year", value_name="TotalEmission")
    filepath = Path('./clean/clean_total_emission_by_country.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    emission_countries_yearly.to_csv(filepath)


if __name__ == '__main__':
    clean_emission_data()
    clean_temperature_data()
