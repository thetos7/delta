import pandas as pd

def get_unemployment():
    tab = pd.read_csv("data/unemployment-rate.csv").rename(columns={'Entity': 'Country', 'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'Unemployment rate %'}).set_index('Country')
    mask = (tab['Year'] >= 2012) & (tab['Year'] <= 2021)
    df = tab[mask].reset_index()
    del df['Code']
    df = df.dropna()
    return df

# Unemployment rate % 0    2.5    5    7.5    10    12.5    15    17.5    20    25    100
# Happiness           10    9     8     7      6      5      4      3      2     1     0
# index = index_sup - (x - index_inf) / (index_sup - index_inf)
def get_index(x, rate_inf, rate_sup, index_sup):
    return index_sup - (x - rate_inf) / (rate_sup - rate_inf)

def transform_rate_to_index(x):
    rate_index = {0: 10,
                  2.5: 9,
                  5: 8,
                  7.5: 7,
                  10: 6,
                  12.5: 5,
                  15: 4,
                  17.5: 3,
                  20: 2,
                  25: 1,
                  100: 0}
    if x in rate_index:
        return rate_index[x]
    else:
        rate_index = list(rate_index.items())
        rate_inf = 0
        rate_sup = 2.5
        index_sup = 10
        for i in range(1, len(rate_index)):
            if rate_index[i][0] < x:
                rate_inf = rate_index[i][0]
                rate_sup = rate_index[i+1][0]
                index_sup = rate_index[i][1]
            else:
                break
    res = get_index(x, rate_inf, rate_sup, index_sup)
    return res

# rule: more unemployment => less happiness
def unemployment_out_of_ten():
    df = get_unemployment()
    df['Unemployment rate %'] = df['Unemployment rate %'].apply(transform_rate_to_index)
    df['Year'] = df['Year'].astype(int)
    return df.rename(columns={'Unemployment rate %': 'Unemployment index'})