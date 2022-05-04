from itertools import dropwhile
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

class EnergyMix():

    def make_dataframe(self):
        energymix = pd.read_csv("./data/World_Energy_Consumption.csv", sep=",", skiprows=[], header=0)
        energymix = energymix.fillna(0.0)
        self.countries = energymix.country.unique()
        energymix = energymix.set_index('country')
        return energymix
    
    def __init__(self, application=None):
        self.energymix = self.make_dataframe()
        
        self.productions = self.energymix[['year', 'fossil_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity']]
        self.productions = self.productions.rename(columns={'fossil_electricity' : 'Fossile', 'hydro_electricity' : 'Hydraulique', 'solar_electricity' : 'Solaire', 'wind_electricity' : 'Eolienne', 'nuclear_electricity' : 'Nucléaire'})
        self.productions = self.productions[self.productions.year >= 1985]
        
        self.coal_use = self.energymix[['iso_code', 'year', 'coal_elec_per_capita']]
        self.coal_use = self.coal_use.rename(columns={'coal_elec_per_capita' : 'KWh de charbon par habitant'})
        self.coal_use = self.coal_use[self.coal_use.year >= 1985]
        self.coal_use = self.coal_use[self.coal_use.iso_code != 0]
        self.coal_use = self.coal_use[self.coal_use.iso_code != 'OWID_WRL']

        self.main_layout = html.Div(children=[
            html.H3(children='Mix énergétique de différents pays du monde'),
            html.Div([ dcc.Graph(id='graph1'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Pays / Zone géographique'),
                           dcc.Dropdown(
                               id='graph1_countries',
                               options=self.countries,
                               value='France',
                               searchable=True,
                               clearable=False
                           )
                         ], style={'width': '9em'} )
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
            }),
            html.Br(),
            html.H3(children="Plus grands pays consommateurs de charbon pour leur alimentation électrique"),
            html.Div([dcc.Graph(id='graph2'), ], style={'width': '100%'}),
            html.Div([
                html.Div([html.Div('Année'),
                            dcc.Dropdown(
                                id='graph2_year',
                                options=[i for i in range(1985, 2019)],
                                value=2017,
                                clearable=False
                            )], style={'width': '9em'}
                            )
            ], style={
                        'padding': '10px 50px', 
                        'display':'flex',
                        'flexDirection':'row',
                        'justifyContent':'flex-start',
                    })
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
                    dash.dependencies.Output('graph1', 'figure'),
                    [ dash.dependencies.Input('graph1_countries', 'value')])(self.update_graph1)
        self.app.callback(
                    dash.dependencies.Output('graph2', 'figure'),
                    [ dash.dependencies.Input('graph2_year', 'value')])(self.update_graph2)
        
    def update_graph1(self, country):
        fig = px.area(self.productions.loc[country], 'year', ['Fossile', 'Hydraulique', 'Solaire', 'Eolienne', 'Nucléaire'],
            title = None,
                labels ={
                    "year": "Année",
                    "value": "Quantité d'énergie générée en TWh",
                    "variable": "Type de source"
                })
        return fig
    
    def update_graph2(self, year):
        fig = px.choropleth(self.coal_use[self.coal_use.year == year], locations='iso_code', color='KWh de charbon par habitant', color_continuous_scale=px.colors.sequential.turbid,
            title = None,
                labels ={
                })
        return fig
        
if __name__ == '__main__':
    nrg = EnergyMix()
    nrg.app.run_server(debug=True, port=8051)