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
import plotly.offline as py
from pandas import DataFrame

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def draw_globe_graph(countries, lst: list, emission: bool):
    if emission:
        data = [
            dict(type='choropleth', locations=countries, z=lst, locationmode='country names', text=countries,
                 marker=dict(line=dict(color='rgb(0,0,0)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='Mean\nEmission,\n(MtCO₂e)'))]
        layout = dict(title='Mean CO2 emission in countries (1990 - 2018)',
                      geo=dict(showframe=False, showocean=True, oceancolor='rgb(0,255,255)',
                               projection=dict(type='orthographic', rotation=dict(lon=60, lat=10), ),
                               lonaxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)'),
                               lataxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)')), )
        return dict(data=data, layout=layout)
    else:
        data = [
            dict(type='choropleth', locations=countries, z=lst, locationmode='country names', text=countries,
                 marker=dict(line=dict(color='rgb(0,0,0)', width=1)),
                 colorbar=dict(autotick=True, tickprefix='', title='# Temperature \nDifferences,\n°C'))]
        layout = dict(title='Temperature differences in countries (1900 - 2013)',
                      geo=dict(showframe=False, showocean=True, oceancolor='rgb(0,255,255)',
                               projection=dict(type='orthographic', rotation=dict(lon=60, lat=10), ),
                               lonaxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)'),
                               lataxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)')), )
        return dict(data=data, layout=layout)


def get_temp_diff(df: DataFrame):
    print(df.columns)
    countries = np.unique(df[df['Country'] != 'World']['Country'])
    temp_dif_lst = []
    for country in countries:
        country_temp = df[(df['Country'] == country) & (
                (df['Year'] == 2013) | (df['Year'] == 1900))][
            'AverageTemperature'].diff()
        country_temp.drop(index=country_temp.index[0], axis=0,
                          inplace=True)
        temp_dif_country = country_temp.values
        if len(temp_dif_country) > 0:
            temp_dif_lst.append(temp_dif_country[0])
    return countries, temp_dif_lst


def get_mean_emission(df: DataFrame):
    countries_emission = np.unique(df[df['Country'] != 'World']['Country'])
    mean_emission_lst = []
    for country in countries_emission:
        mean_total_emission = df[(df['Country'] == country)]['Mean']
        if len(mean_total_emission.values) > 0:
            mean_emission_lst.append(mean_total_emission.values[0])
    return countries_emission, mean_emission_lst


def load_cleaned_dataframe_from_csv(filename: str, cols: int):
    return pd.read_csv(filename, usecols=[i for i in range(1, cols)])


class GlobalWarming:

    def __init__(self, application=None):
        clean_temp_df = load_cleaned_dataframe_from_csv(
            "data/clean/clean_global_land_temperature_by_country.csv", cols=4)
        clean_emission_df = load_cleaned_dataframe_from_csv(
            "data/clean/clean_total_emission_by_country.csv", cols=4)
        clean_mean_emission_df = load_cleaned_dataframe_from_csv("data/clean/clean_mean_emission_by_country.csv",
                                                                 cols=36)
        clean_temp_df.dropna(inplace=True)
        clean_emission_df.dropna(inplace=True)

        self.clean_emission_df = clean_emission_df.copy()
        self.clean_temp_df = clean_temp_df.copy()

        # Drawing globe graph
        countries, temp_def_lst = get_temp_diff(clean_temp_df)
        fig_temp = draw_globe_graph(countries, temp_def_lst, False)

        countries_emission, mean_emission_lst = get_mean_emission(clean_mean_emission_df.iloc[1:, :])
        fig_emission = draw_globe_graph(countries_emission, mean_emission_lst, True)

        fig_line_us = self.draw_line_graph("United States")

        self.countries = np.unique(clean_temp_df.Country)
        self.main_layout = html.Div(children=[
            html.Div(children=[html.Div([dcc.Graph(figure=fig_temp), ], style={'width': '100%', }),
                               html.Br(),
                               html.Div([dcc.Graph(figure=fig_emission), ], style={'width': '100%', }),
                               html.Br()], style={
                'display': 'flex'
            }),
            html.Div([html.Div('Countries'),
                      dcc.Dropdown(
                          id='glb-which-countries',
                          options=[{'label': country, 'value': country} for country in self.countries],
                          value='World',
                      ),
                      ], style={'width': '25%', 'padding': '2em 0px 0px 0px'}),
            html.Div([dcc.Graph(figure=fig_line_us, id='glb-line-graph'), ], style={'width': '100%', }),
            html.Br(),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
        self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('glb-line-graph', 'figure'),
            [dash.dependencies.Input('glb-which-countries', 'value')]
        )(self.draw_line_graph)

    def draw_line_graph(self, country: str):
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        country_temp = self.clean_temp_df[self.clean_temp_df.Country == country]
        country_emission = self.clean_emission_df[self.clean_emission_df.Country == country]

        fig.add_trace(go.Scatter(x=country_temp.Year, y=country_temp.AverageTemperature, name="Average Temperature"),
                      secondary_y=False)

        fig.add_trace(go.Scatter(x=country_emission.Year, y=country_emission.TotalEmission, name="Total Emission"),
                      secondary_y=True)

        fig.update_layout(title_text="Average Temperature and Total Emission of " + country)
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Temperature", secondary_y=False)
        fig.update_yaxes(title_text="Total Emission", secondary_y=True)
        return fig


if __name__ == '__main__':
    nrg = GlobalWarming()
    nrg.app.run_server(debug=True, port=8051)
