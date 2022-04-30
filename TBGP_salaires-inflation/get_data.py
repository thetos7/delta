import pandas as pd
import numpy as np

infl_conv = {
    'AUS': 'AU',
    'AUT': 'AT',
    'BEL': 'BE',
    'CAN': 'CA',
    'CZE': 'CZ',
    'DNK': 'DK',
    'FIN': 'FI',
    'FRA': 'FR',
    'DEU': 'DE',
    'GRC': 'GR',
    'HUN': 'HU',
    'ISL': 'IS',
    'IRL': 'IE',
    'ITA': 'IT',
    'JPN': 'JP',
    'KOR': 'KR',
    'LUX': 'LU',
    'MEX': 'MX',
    'NLD': 'NL',
    'NZL': 'NZ',
    'NOR': 'NO',
    'POL': 'PL',
    'PRT': 'PT',
    'SVK': 'SK',
    'ESP': 'ES',
    'SWE': 'SE',
    'TUR': 'TR',
    'GBR': 'GB',
    'USA': 'US',
    'BRA': 'BR',
    'CHL': 'CL',
    'CHN': 'CN',
    'EST': 'EE',
    'IND': 'IN',
    'IDN': 'ID',
    'ISR': 'IL',
    'RUS': 'RU',
    'SVN': 'SI',
    'ZAF': 'ZA',
    'OECD': 'TOT',
    'COL': 'CO',
    'LVA': 'LV',
    'SAU': 'SA',
    'EA19': 'EA',
    'ARG': 'AR',
    'LTU': 'LT',
    'EU27_2020': 'EU27_2020'
}

def fill_missing_years(wages, countries):
    tmp_wages = wages.set_index('year')
    to_add = pd.DataFrame()

    for country in countries:
        c = tmp_wages[(tmp_wages.country == country) & (tmp_wages.age == 'TOTAL') & (tmp_wages.sex == 'T')]
        if (not c.empty):
            r = pd.date_range(start=c.index.min(), end=c.index.max(), freq='YS')

            filled = c.reindex(r, fill_value=np.nan).rename_axis('year')
            rows_to_add = filled[filled['age'].isna()].index
            filled = filled.interpolate(method='time').fillna(method='ffill')

            if (not rows_to_add.empty):
                to_add = pd.concat([to_add, filled.loc[rows_to_add].reset_index()],ignore_index = True, axis=0)

    return pd.concat([wages, to_add], ignore_index=True, axis=0)

def clean_inflation(inflation):
    inflation.LOCATION = inflation.LOCATION.apply(lambda s: infl_conv[s])
    inflation.rename({'LOCATION': 'country', 'TIME': 'year'}, axis='columns', inplace=True)
    return inflation

def clean_wages(wages):
    wages = wages[wages.indic_il == 'MED_E']
    wages = wages[wages.unit == 'EUR']
    wages.geo[wages.geo == 'UK'] = 'GB'
    wages.rename({'geo': 'country', 'TIME_PERIOD': 'year', }, axis='columns', inplace=True)
    wages.drop(['indic_il', 'unit'], axis='columns', inplace=True)
    return wages

def get_country_cumulative(inflation, min_year, country):
    df = inflation[(inflation.country == country) & (inflation.year >= min_year)]
    res = (df.Value / 100 + 1).cumprod()
    res /= df.iloc[0, 2] / 100 + 1
    return res


def compute_cumulative(inflation, wages):
    countries = inflation.country.unique()
    for country in countries:
        min_year = inflation[inflation.country == country].iloc[0,1] if wages[wages.country == country].empty else max(inflation[inflation.country == country].iloc[0,1], wages[wages.country == country].iloc[0,3])
        inflation.loc[(inflation.country == country) & (inflation.year >= min_year),'cumulative_sum'] = get_country_cumulative(inflation, min_year, country)
    return inflation

def merge_dataframes(inflation, wages):
    ret = pd.merge(inflation, wages, how='left', on=['year', 'country'])
    ret.rename({'Value': 'inflation_value', 'OBS_VALUE': 'wages_value'}, axis='columns', inplace=True)
    ret.dropna(inplace=True)
    return ret

def get_data():
    wages = pd.read_csv('data/salaires.csv', usecols=['age', 'sex', 'indic_il', 'unit', 'geo', 'TIME_PERIOD', 'OBS_VALUE'], parse_dates=['TIME_PERIOD'])
    inflation = pd.read_csv('data/inflation.csv', usecols=['LOCATION', 'TIME', 'Value'], parse_dates=['TIME'])

    inflation, wages = clean_inflation(inflation), clean_wages(wages)
    wages = fill_missing_years(wages, inflation.country.unique())

    return merge_dataframes(compute_cumulative(inflation, wages), wages)
