import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from scipy import stats
from scipy import fft


class Pollution():
    def __init__(self, application=None):

        # getting pollution
        pollution = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/pollution.pkl')
        COfig = px.line(pollution, y="CO Mean", title='CO per day')
        NO2fig = px.line(pollution, y="NO2 Mean", title='NO2 per day')
        O3fig = px.line(pollution, y="O3 Mean", title='O3 per day') # not produced by cars, but byproduct of NO2 under UV light
        SO2fig = px.line(pollution, y="SO2 Mean", title='SO2 per day') # not rejected by cars

        # getting prices
        prices = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/prices.pkl')
        pricesFig = px.line(prices, x='Date', y='Gasoline Dollars per Gallon', title='Gas price per week')

        # getting average temp + precipitation
        average_cities = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/average_cities.pkl')
        celsiusFig = px.line(average_cities, x="Date", y="average_celsius", title='average_celsius')
        prcpFig = px.line(average_cities, x="Date", y="prcp_cm", title='prcp_cm')

        self.main_layout = html.Div(children=[
            html.H3(children='Pollution/Petrole'),
            html.Div([ dcc.Graph(figure=COfig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=NO2fig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=O3fig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=SO2fig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=pricesFig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=celsiusFig), ], style={'width':'100%', }),
            html.Div([ dcc.Graph(figure=prcpFig), ], style={'width':'100%', }),
            html.Br(),
            dcc.Markdown("""Space Movie 1992""")
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


if __name__ == '__main__':
    pol = Pollution()
    pol.app.run_server(debug=True, port=8051)
