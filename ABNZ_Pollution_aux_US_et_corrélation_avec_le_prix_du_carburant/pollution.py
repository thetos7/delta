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

import ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant.get_data as dfdata


class Pollution():
    def __init__(self, application=None):
        self.df = pd.read_pickle('ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant/data/prices.pkl')

        self.main_layout = html.Div(children=[
            html.H3(children='Pollution/Petrole'),
            html.Div([ dcc.Graph(id='mpj-main-graph'), ], style={'width':'100%', }),
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
