from gc import get_count
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

    def init_caracteristiques(self):
        df = pd.read_csv('spotify/data/SpotifyFeatures.csv')
        df = df.rename(columns={'artist_name':'artist', 'track_name':'title'})
        
        dfmean = df.drop(columns=['artist', 'title', 'track_id', 'key', 'mode', 'time_signature'])
        dfmean = dfmean.groupby(['genre']).mean()
        dfmean = dfmean.drop(index=['Children\'s Music'])
        self.caracteristiques = dfmean

        count = []
        for genre in dfmean.index:
            count.append(np.sum(df.genre == genre))
        self.count = count

    def __init__(self, application = None):
        self.french = {'popularity':'popularité', 'acousticness':'accoustique', 'danceability':'dansabilité', 'duration_ms':'temps en ms',
        'energy':'énergie', 'instrumentalness':'instrumentalité', 'liveness':'vivacité', 'loudness':'intensité sonore', 'speechiness':'quantité de paroles',
        'tempo':'tempo', 'valence':'valence'}

        self.init_caracteristiques()

        self.main_layout = html.Div(children=[
            html.H3(children='Caractéristiques de la popularité d\'une musique sur Spotify'),
            html.Div([
                html.Div([ dcc.Graph(id='carac-main-graph'), ], style={'width':'85%'}),
                
                html.Div([ 
                    html.Div('Caractéristique axe x'),
                    dcc.RadioItems(
                        id='x-carac',
                        options=[{'label':self.french[self.caracteristiques.columns[i]], 'value':i} for i in range(len(self.caracteristiques.columns))],
                        value=2,
                        labelStyle={'display':'block'},
                        )
                    ], style={'margin-left':'30px', 'margin-top':'100px','width': '10em', 'float':'right'} )
                ], style={
                    'padding-right': '30px', 
                    'display':'flex'
                }),
            html.Div([ 
                    html.Div('Échelle'),
                    dcc.RadioItems(
                        id='log',
                        options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                        value='Linéaire',
                        labelStyle={'display':'block'},
                        )
                    ]),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
                #### Notes :
                    
                La popularité d'un genre est un pourcentage. Celle d'une musique correspond à son nombre d'écoutes par rapport au nombre d'écoutes de la musique la plus écoutée.
                Ainsi, la valeur utilisée correspond à la moyenne des popularités des musiques d'un genre
                
                Les autres caractériques du graphique sont définies à cette adresse : [Caractéristiques audio d'une musique](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)
                """),
            html.Br(),
            dcc.Markdown("""
                #### À propos

                * Sources : 
                    * [Caractéristiques et popularité des musiques de Spotify](https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db) sur kaggle.com
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
                    dash.dependencies.Output('carac-main-graph', 'figure'),
                    dash.dependencies.Input('x-carac', 'value'),
                    dash.dependencies.Input('log', 'value')
                    )(self.update_graph)

    def update_graph(self, x_carac, log):
        df = self.caracteristiques
        log = log == 'Log'
        fig = px.scatter(df, x=df.columns[x_carac], y='popularity', color=df.index, hover_name=df.index, log_x=log,
                         title="Popularité des genres en fonction de certaines caractéristiques",
                         labels={
                            'popularity': 'popularité',
                            df.columns[x_carac]: self.french[df.columns[x_carac]]
                        },
                        size=self.count,
                        height=750,
                    )
        return fig

if __name__ == '__main__':
    spo = Spotify()
    spo.app.run_server(debug=True, port=8051)