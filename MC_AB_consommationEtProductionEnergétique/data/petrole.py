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

        print(self.impor[self.impor.TIME_PERIOD == 1990].groupby("geo")["OBS_VALUE"].sum())

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
                               value=years[0],
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
        df = self.impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()
        print(f"year: {year}")
        print(f"max: {df}")

        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig



if __name__ == '__main__':
    ind = Independance_Petrole()
    ind.app.run_server(debug=True, port=8051)
