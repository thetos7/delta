import sys

from requests import NullHandler
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

class Spotify():

    def format_caracteristiques():
        df = pd.read_csv('spotify/data/SpotifyFeatures.csv')
        df = df.rename(columns={'artist_name':'artist', 'track_name':'title'})
        dfmean = df.drop(columns=['artist', 'title', 'track_id', 'key', 'mode', 'time_signature'])
        dfmean = dfmean.groupby(['genre']).mean()
        return dfmean

    def __init__(self, application = None):
        self.caracteristiques = Spotify.format_caracteristiques()

        self.main_layout = html.Div(children=[
            html.H3(children='Caractéristiques de la popularité d\'une musique sur Spotify'),
            html.Div([ dcc.Graph(id='spo-main-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Spotify'),
                           dcc.RadioItems(
                               id='spo-spo',
                               options=[{'label':'Oui', 'value':0}, 
                                        {'label':'Non','value':1}],
                               value=1,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} )
                    ]),
            html.Br(),
            dcc.Markdown("""
                #### À propos

                * Sources : 
                    * [Caréctéristiques et popularité des musiques de Spotify](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) sur kaggle.com
                    * [Informations complémentaires sur la popularité, la date, ou la région](https://www.kaggle.com/datasets/dhruvildave/spotify-charts) sur kaggle.com
                * (c) 2022 Thibaut Ambrosino, Melvin Gidel
                """)
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
                    dash.dependencies.Output('spo-main-graph', 'figure'),
                    dash.dependencies.Input('spo-spo', 'value'))(self.update_graph)

    def update_graph(self, spo):
        df = self.caracteristiques
        fig = px.scatter(df, x='popularity', y='danceability', color=df.index, hover_name=df.index, log_x=False,
                         title="Popularity of genres through the dance"
                        )
        return fig

if __name__ == '__main__':
    spo = Spotify()
    spo.app.run_server(debug=True, port=8051)