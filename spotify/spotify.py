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

class Spotify():
    def _make_dataframe(filename):
        df = pd.read_csv(filename, sep=";", encoding="cp1252", skiprows=[0,1,3], header=None)
        return df

    def __init__(self, application = None):

        self.main_layout = html.Div(children=[
            html.H3(children='Caractéristiques de la popularité d\'une musique sur Spotify'),
            html.Div([ dcc.Graph(id='spo-main-graph'), ], style={'width':'100%', }),
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

        

if __name__ == '__main__':
    spo = Spotify()
    spo.app.run_server(debug=True, port=8051)