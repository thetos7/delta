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
import geojson
import plotly.graph_objects as go

from get_data import get_data
from get_data import get_by_year
from get_data import list_years
from get_data import list_countries


class Independance_Petrole():
    def __init__(self, application=None):

        self.prod_cons, self.export, self.impor = get_data()
   
        years = list_years(self.impor)

        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""Independance Européene face au Petrole comme energie fossile"""),
            html.Div([ html.Div('Année ref.'),
                          dcc.Dropdown(
                               id='nrg-which-year',
                               options=[{'label': i, 'value': i} for i in years],
                               value=1,
                               disabled=False,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
        html.Div([ dcc.Graph(id='nrg-main-graph'), ], style={'width':'100%', }),
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
                    dash.dependencies.Output('nrg-main-graph', 'figure'),
                    [dash.dependencies.Input('nrg-which-year', 'value')])(self.update_graph)
    
    def update_graph(self, year):
        with open("resources/custom.geo.json", "r", encoding="utf-8") as f: # https://geojson-maps.ash.ms/
            geometry = geojson.load(f)

        locs = list_countries(self.impor)
        fig = go.Figure([
            go.Choropleth(
                geojson = geometry,
                locations = locs,
                text = locs
        )])

        fig.update_geos(
            fitbounds="locations",
            resolution=50,
            visible=True,
            showframe=False,
            projection={"type": "mercator"},
        )
        return fig



if __name__ == '__main__':
    ind = Independance_Petrole()
    ind.app.run_server(debug=True, port=8051)
