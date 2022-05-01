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
import plotly.express as px

from get_data import get_data
from get_data import get_by_year
from get_data import list_years
from get_data import list_countries


class Independance_Petrole():
    def __init__(self, application=None):

        self.prod_cons, self.export, self.impor = get_data()
   
        years = list_years(self.impor)

        with open("resources/custom.europe.geojson", "r", encoding="utf-8") as f: # https://geojson-maps.ash.ms/
            self.europe = geojson.load(f)

        for i in self.europe["features"]:
            fips = i["properties"]["iso_a2"]
            print(fips)
            i["id"] = fips

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
        html.Div([ dcc.Graph(id='nrg-main-graph'), ], style={ }),
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
        fig = px.choropleth_mapbox(self.impor, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(-1, 1),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig



if __name__ == '__main__':
    ind = Independance_Petrole()
    ind.app.run_server(debug=True, port=8051)
