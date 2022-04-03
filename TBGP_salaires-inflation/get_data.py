import pandas as pd

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

def get_data():
    wages = pd.read_csv('data/salaires.csv', usecols=['age', 'sex', 'indic_il', 'unit', 'TIME_PERIOD', 'OBS_VALUE'])
    inflation = pd.read_csv('data/inflation.csv', usecols=['LOCATION', 'TIME', 'Value'])
    inflation.LOCATION = inflation.LOCATION.apply(lambda s: infl_conv[s])
    return inflation, wages