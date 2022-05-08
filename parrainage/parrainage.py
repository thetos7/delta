import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import json

from parrainage.get_data import fetch_data

class Parrainage():

    def __init__(self, application = None):
        fetch_data()
        self.df = pd.read_csv("parrainage/data/parrainagestotal.csv", sep=";")
        self.candidats_occurences = self.df['Candidat'].value_counts()
        self.candidats_list = self.candidats_occurences[self.candidats_occurences > 500].keys()

        with open("parrainage/data/departements.geojson") as f:
            self.departements_json = json.load(f)
        
        self.main_layout = html.Div(children=[
            html.H3(children='Évolution du nombre de parrainages par candidat à la présidentielle'),

            html.Div([
                    html.Div([ dcc.Graph(id='par-main-graph'), ], style={'width':'80%', }),
                    html.Div([
                        html.Br(),
                        html.Br(),
                        html.Div('Candidat'),
                        dcc.RadioItems(
                            id='par-candidat',
                            options=[{'label': candidat, 'value': candidat} for candidat in self.candidats_list],
                            value=self.candidats_list[0],
                            labelStyle={'display':'block'},
                        ),
                        html.Br()
                    ], style={'margin-left':'15px', 'width': '15em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            html.Br(),
            html.Div([ dcc.Graph(id='par-main-map') ], style={'width':'100%'}),    
            dcc.Markdown("""
                # Sources
                    * [Jeu de données parrainage des candidats pour l'élection présidentielle 2022](https://www.data.gouv.fr/fr/datasets/parrainages-des-candidats-a-lelection-presidentielle-francaise-de-2022/)
                    * [GeoJSON France (délimitations géographiques des départements)](https://france-geojson.gregoiredavid.fr/)
                # Auteurs
                    * Nathan Cabasso (<nathan.cabasso@epita.fr>)
                    * Ferdinand Mom (<ferdinand.mom@epita.fr>)
            """),
        ], style={
                #'backgroundColor': 'rgb(240, 240, 240)',
                 'padding': '10px 50px 10px 50px',
                 }
        )

        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('par-main-graph', 'figure'),
            [dash.dependencies.Input('par-candidat', 'value')]
        )(self.update_graph)

        self.app.callback(
            dash.dependencies.Output('par-main-map', 'figure'),
            [dash.dependencies.Input('par-candidat', 'value')]
        )(self.display_map)
    
        

    def update_graph(self, candidat):
        # Select candidate
        parrainages = self.df[self.df['Candidat'] == candidat]

        count_by_date = parrainages.groupby(["Date de publication"]).size()

        index = count_by_date.index
        index.name = 'date'

        df_count_by_date = pd.DataFrame(
            {"Parrainages ce jour": count_by_date, "Parrainages total": count_by_date.cumsum()}, index=index)

        df_count_by_date = df_count_by_date.reset_index().melt('date', var_name="Catégorie", value_name="y")

        fig = px.line(df_count_by_date, template='plotly_white', x='date', y='y', color='Catégorie')
        fig.update_traces(hovertemplate='%{y} parrainages le %{x:%d/%m/%y}')
        fig.update_layout(hovermode="x unified")
        fig.update_layout(
            xaxis = dict(title="Date de publication"),
            yaxis = dict(title="Nombre parrainages"), 
            height=450,
            showlegend=True,
        )

        return fig
    
    def display_map(self, candidat):
        
        candidat_df = self.df[self.df['Candidat'] == candidat]
        department_candidat_df = candidat_df.groupby("Département")
        candidat_repertition_per_departement = department_candidat_df["Département"].count().to_frame(name="Score").reset_index()

        fig_map = px.choropleth_mapbox(
            candidat_repertition_per_departement,
            geojson=self.departements_json,
            locations='Département',
            featureidkey="properties.nom",
            mapbox_style='carto-positron',
            color="Score",
            color_discrete_sequence=[1],
            hover_data={'Score': True},
            zoom=3.8,
            center={'lat': 47, 'lon': 2},
            opacity=1.0,
        )

        fig_map.update_layout(
            title={
                'text': f'Parrainage de "{candidat}" par département',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        return fig_map

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ws = Parrainage()
    ws.run(port=8055)
