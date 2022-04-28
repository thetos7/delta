import numpy as np
import pandas as pd
import matplotlib
import glob
import plotly.express as px
from os import listdir
#First We are going to create the different groups that we are going to be using
#throughout the code

colnames = ["Sex", "Type of Cancer","Age group", "Number of cases","person-years at risk"]

path_africa = "CI5_treated_data/AFRICA/"
path_europe = "CI5_treated_data/EUROPE/"
path_north_america = "CI5_treated_data/NORTH-AMERICA/"
path_south_america = "CI5_treated_data/SOUTH-AMERICA/"
path_asia = "CI5_treated_data/ASIA/"
path_oceania = "CI5_treated_data/OCEANIA/"

Africa_list = []
Europe_list = []
North_america_list = []
South_america_list = []
Asia_list = []
Oceania_list = []

#Function to create Dataframe 
def create_df_country(df_path, df_name):
    all_files = glob.glob(df_path+df_name+"/*.csv")
    list_Country = [pd.read_csv(files,header=None,names=colnames) for files in all_files]
    Country = pd.concat(list_Country)
    modify_cancer_value(Country)
    Country = Country[Country['Type of Cancer'].str.contains("total|Unspecified")==False]
    return Country

def create_df_continent(df_path):
    list_Country = []
    for f in listdir(df_path):
        current_country = create_df_country(df_path,f)
        list_Country.append(current_country)
    Continent = pd.concat(list_Country)
    return Continent

def create_hist(current_df, column_x, column_y, column_color, marginal_option):
    df = px.data.tips()
    if marginal_option == 'violin' or marginal_option == 'rug' or marginal_option == 'box':
        fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},marginal=marginal_option,text_auto=True)
    else:
        fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},text_auto=True)
    fig.show()

#Create dash application 
from dash import Dash, dcc, html, Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True)