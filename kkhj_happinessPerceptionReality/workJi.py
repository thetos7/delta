import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

from cleanUnemploymentData import *
from cleanSocialSecurityContributionData import *
from cleanSafetyData import *



def extract_safety(year):
    file = "data/criminality" + str(year) + ".xlsx"
    tab = pd.read_excel(file)
    df = pd.DataFrame({'Country': tab["Country"], f"{year}": tab["Safety Index"]})
    return df

def get_safety():
    tab = extract_safety(2012)
    for x in range(13, 22):
        file = str(20) + str(x)
        tab = tab.join(extract_safety(file).set_index(['Country']), on='Country')
    return tab.melt(['Country'], var_name='Year', value_name='Safety Index')

def safety_out_of_10():
    tab = get_safety()
    tab['Safety Index'] = tab['Safety Index'].div(10)
    return tab

# TODO modify url social security contributions https://home.kpmg/xx/en/home/services/tax/tax-tools-and-resources/tax-rates-online/social-security-employer-tax-rates-table.html
# TODO modify url unemployment

def get_security_contribution():
    df = pd.read_excel("data/socialSecurityContributions.xlsx")
    df = df.melt(['Country'], var_name='Year', value_name='Social Security Employer Contribution')
    return df[(df != '-').all(1)]

def security_contribution_out_of_10():
    df = get_security_contribution()
    df.loc[:, df.columns == 'Social Security Employer Contribution'] = df.loc[:, df.columns == 'Social Security Employer Contribution'].div(10)
    return df

def get_unemployment():
    tab = pd.read_csv("data/unemployment-rate.csv").rename(columns={'Entity': 'Country', 'Unemployment, total (% of total labor force) (modeled ILO estimate)': 'Unemployment rate %'}).set_index('Country')
    mask = (tab['Year'] >= 2012) & (tab['Year'] <= 2021)
    df = tab[mask].reset_index()
    del df['Code']
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
    return df.rename(columns={'Unemployment rate %': 'Unemployment index'})


# print(unemployment_out_of_ten()["Year"])
# print(safety_out_of_10()['Year'])
safety = safety_out_of_10()
unemployment = unemployment_out_of_ten()
# print(safety['Year'])
# print(unemployment['Year'])
df = pd.merge(unemployment, safety, how="inner", on=["Country", "Year"])
df = pd.merge(security_contribution_out_of_10(), df, how="inner", on=["Country", "Year"])
mask2 = ((unemployment.groupby('Country')).size() >= 9)
# # pd.set_option('display.max_rows', df.shape[0]+1)
# # pd.set_option('display.max_columns', df.shape[1]+1)
# df = df[df[mask2.reindex(df.index, fill_value=False)]]
mask2.to_excel("output.xlsx")