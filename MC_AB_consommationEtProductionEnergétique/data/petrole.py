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
import plotly.express as px
import json
import math

from get_data import get_data
from get_data import get_by_year
from get_data import list_years
from get_data import list_countries
from get_data import country_code


class Independance_Petrole():
    def __init__(self, application=None):

        self.prod, self.cons, self.export, self.impor = get_data()
   
        self.years = list_years(self.impor)

        self.partners = [item for item in self.impor["partner"].unique() if item == item]
        self.countries = [item for item in self.impor["geo"].unique() if item == item]

        with open("resources/europe.geo.json", "r", encoding="utf-8") as f: # https://geojson-maps.ash.ms/
            self.europe = json.load(f)

        for i in self.europe["features"]:
            fips = i["properties"]["iso_a2"]
            i["id"] = fips
        
        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""Independance Européene face au Petrole comme energie fossile"""),
            html.Div([ html.Div('Année ref.'),
                          dcc.Slider(0, len(self.years) -1, 1,
                               id='year',
                               marks={i: str(self.years[i]) for i in range(len(self.years))},
                               value=len(self.years) // 2
                           ),
                           html.Div('Selectionner les pays dont on souhaite stopper les exportations'),
                           dcc.Dropdown(
                               id='excluded-countries',
                               options=[{"label":country_code[i], "value": i} for i in self.partners],
                               value=[],
                               multi=True
                           ),
                         ], style={'position': 'sticky', 'top': 0, 'zIndex': 1, 'backgroundColor': 'white', 'width': '100%', 'padding':'4em 0px 0px 0px'}), # bas D haut G
            html.Div([
                html.Div([
                    html.H2('Importations de petrole par pays:'),
                    html.Div([ dcc.Graph(id='import-graph'), ], style={'width': '55em' })]),
                html.Div([
                    html.H2('Exportations de petrole par pays:'),
                    html.Div([ dcc.Graph(id='export-graph'), ], style={'width': '55em'})])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.H2('Consommation de petrole par pays:'),
                    html.Div([ dcc.Graph(id='cons-graph'), ], style={'width': '55em' })]),
                html.Div([
                    html.H2('Production de petrole par pays:'),
                    html.Div([ dcc.Graph(id='prod-graph'), ], style={'width': '55em'})])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.H2('Excedent de petrole par pays, calculé par Exc = production + importation - exportation - consommation :'),
                    html.Div([ dcc.Graph(id='rel-graph'), ], style={'width': '110em' })])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                html.Div([
                    html.H2('Les plus gros importateurs de pétrole:'),
                    html.Div([ dcc.Graph(id='big-import-graph'), ], style={'width': '110em' })])
            ], style={'display': 'flex', 'justify-content': 'space-between'}),
            html.Div([
                    html.Div([
                        'Selectionner le pays dont on souhaite voir d\'ou viennent les importations',
                        dcc.Dropdown(
                            id='specific-importation-of-country',
                            options=[{"label":country_code[i], "value": i} for i in self.countries]
                           ),
                    html.Div([ dcc.Graph(id='specific-import-graph'), ], style={'width': '110em' })])
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
                    [dash.dependencies.Input('year', 'value'),
                    dash.dependencies.Input('excluded-countries', 'value')])(self.update_graph_export)
        self.app.callback(
                    dash.dependencies.Output('cons-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_cons)
        self.app.callback(
                    dash.dependencies.Output('prod-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value')])(self.update_graph_prod)
        self.app.callback(
                    dash.dependencies.Output('rel-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value'),
                    dash.dependencies.Input('excluded-countries', 'value')])(self.update_graph_reliability)
        self.app.callback(
                    dash.dependencies.Output('big-import-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value'),
                    dash.dependencies.Input('excluded-countries', 'value')])(self.update_biggest_importators)
        self.app.callback(
                    dash.dependencies.Output('specific-import-graph', 'figure'),
                    [dash.dependencies.Input('year', 'value'),
                    dash.dependencies.Input('excluded-countries', 'value'),
                    dash.dependencies.Input('specific-importation-of-country', 'value')])(self.update_importators)
    
    def update_graph_import(self, year):
        year = self.years[year]
        df = self.impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()

        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_export(self, year, excluded_countries):
        year = self.years[year]
        df = self.export[~self.export.geo.isin(excluded_countries)]
        df = df[self.export.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
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
                                color_continuous_scale="Viridis",
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


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="Viridis",
                                range_color=(0, max_val),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_graph_reliability(self, year, excluded_countries):
        year = self.years[year]
        #cons = self.cons[~self.cons.geo.isin(excluded_countries)]
        cons = self.cons[self.cons.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        #prod = self.prod[~self.prod.geo.isin(excluded_countries)]
        prod = self.prod[self.prod.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        #export = self.export[~self.export.geo.isin(excluded_countries)]
        export = self.export[self.export.TIME_PERIOD == year]
        export.loc[export.geo.isin(excluded_countries), "OBS_VALUE"] = 0
        export = export.groupby("geo")["OBS_VALUE"].sum()

        #impor = self.impor[~self.impor.geo.isin(excluded_countries)]
        impor = self.impor[~self.impor.partner.isin(excluded_countries)]
        impor = impor[self.impor.TIME_PERIOD == year].groupby("geo")["OBS_VALUE"].sum()

        df = prod + impor - export - cons
        max_val = max(df)
        df = df.reset_index()


        fig = px.choropleth_mapbox(df, geojson=self.europe, locations='geo', color='OBS_VALUE',
                                color_continuous_scale="RdYlGn",
                                range_color=(-1, 1),
                                mapbox_style="carto-positron",
                                zoom=2, center = {"lat": 55, "lon": 0},
                                opacity=0.5,
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    def update_biggest_importators(self, year, excluded_countries):
        year = self.years[year]
        df = self.impor[~self.impor.partner.isin(excluded_countries)]
        df = df[df.TIME_PERIOD == year].groupby("partner")["OBS_VALUE"].sum()
        df = df.reset_index()
        df = df[df.OBS_VALUE != 0]
        df.sort_values(by=['OBS_VALUE'], inplace=True, ascending=False)

        df['partner'] = df['partner'].apply(lambda x: country_code[x])
        fig = px.scatter(df, x="partner", y="OBS_VALUE")

        return fig

    def update_importators(self, year, excluded_countries, country):
        year = self.years[year]
        df = self.impor[~self.impor.partner.isin(excluded_countries)]
        df = df[df.TIME_PERIOD == year][df.geo == country].groupby("partner")["OBS_VALUE"].sum()
        df = df.reset_index()
        df = df[df.OBS_VALUE != 0]
        df.sort_values(by=['OBS_VALUE'], inplace=True, ascending=False)
        df['partner'] = df['partner'].apply(lambda x: country_code[x])
        fig = px.scatter(df, x="partner", y="OBS_VALUE")

        return fig

    



if __name__ == '__main__':
    ind = Independance_Petrole()
    ind.app.run_server(debug=True, port=8051)
