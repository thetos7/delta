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

        self.prod, self.cons, self.export, self.impor = get_data()
   
        self.years = list_years(self.impor)

        #print(self.impor[self.impor.TIME_PERIOD == 1990].groupby("geo")["OBS_VALUE"].sum())

        with open("resources/europe.geo.json", "r", encoding="utf-8") as f: # https://geojson-maps.ash.ms/
            self.europe = geojson.load(f)

        for i in self.europe["features"]:
            fips = i["properties"]["iso_a2"]
            #print(fips)
            i["id"] = fips
        
        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""Independance Européene face au Petrole comme energie fossile"""),
            html.Div([ html.Div('Année ref.'),
                          dcc.Slider(0, len(self.years) -1, 1,
                               id='year',
                               marks={i: str(self.years[i]) for i in range(len(self.years))},
                               value=1
                           ),
                           #dcc.Dropdown(
                           #    id='year',
                           #    options=[{'label': i, 'value': i} for i in years],
                           #    value=years[0],
                           #    clearable=False
                           #),
                         ], style={'width': '100%', 'padding':'4em 0px 0px 0px'}), # bas D haut G
            html.Div([
                html.Div([
                    html.Div('Importations de petrole par pays:'),
                    html.Div([ dcc.Graph(id='import-graph'), ], style={'width': '55em' })]),
                html.Div([
                    html.Div('Exportations de petrole par pays:'),
                    html.Div([ dcc.Graph(id='export-graph'), ], style={'width': '55em'})])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.Div('Consommation de petrole par pays:'),
                    html.Div([ dcc.Graph(id='cons-graph'), ], style={'width': '55em' })]),
                html.Div([
                    html.Div('Production de petrole par pays:'),
                    html.Div([ dcc.Graph(id='prod-graph'), ], style={'width': '55em'})])
            ], style={'display': 'flex', 'justify-content': 'space-between'})
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
                    dash.dependencies.Output('import-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_import)
        self.app.callback(
                    dash.dependencies.Output('export-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_export)
        self.app.callback(
                    dash.dependencies.Output('cons-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_cons)
        self.app.callback(
                    dash.dependencies.Output('prod-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_prod)
    
    def update_graph_import(self, year):
        year = self.years[year]
        df = self.impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()
        print(f"year: {year}")

        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_export(self, year):
        year = self.years[year]
        df = self.export[self.export.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="RdYlGn",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_cons(self, year):
        year = self.years[year]
        df = self.cons[self.cons.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="RdYlGn",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig
    
    def update_graph_prod(self, year):
        year = self.years[year]
        df = self.prod[self.prod.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()
        print(df)


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="RdYlGn",
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
