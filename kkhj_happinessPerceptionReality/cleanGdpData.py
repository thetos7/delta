import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_dataframe():
    df = pd.read_csv("data/PIB.csv")
    df.rename(columns={'TIME': 'Year'}, inplace=True)
    mask = (df['Year'] >= 2012) & (df['Year'] <= 2021)
    df = df[mask]
    return df

def find_bin_idx_of_value(bins, value):
    array = np.asarray(value)
    idx = np.digitize(array, bins)
    return idx - 1

def area_before_val(counts, bins, val):
    right_bin_edge_index = find_bin_idx_of_value(bins, val)
    bin_width = np.diff(bins)[0]
    area = sum(bin_width * counts[:right_bin_edge_index])
    return area

def get_gdp_value_for_single_value(counts, bins, val, total_area):
    return area_before_val(counts, bins, val) / total_area * 10

#main function
def gdp_out_of_10():
    dataframe = get_dataframe()
    min_year = 2012
    max_year = 2021
    for year in range(min_year, max_year+1):
        year_df = dataframe[dataframe['Year'] == year]
        year_series = pd.Series(year_df['Value'])
        counts, bins, _ = plt.hist(year_series, bins=50, alpha=0.3, density=True, label="Data")
        total_area = sum(np.diff(bins) * counts)
        year_df = year_df.reset_index()
        for index, row in year_df.iterrows():
            location = row['LOCATION']
            value = row['Value']
            gdp_value = get_gdp_value_for_single_value(counts, bins, value, total_area)
            dataframe.loc[(dataframe['Year'] == year) & (dataframe['LOCATION'] == location), ["GDP"]] = gdp_value
    return dataframe