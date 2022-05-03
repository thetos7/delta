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

class RGPD():

    def __init__(self, application = None):
        self.main_layout = html.Div(children=[
            html.H1(children="Évolution de l'application du RGPD en France")
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

if __name__ == '__main__':
    rgpd = RGPD()
    rgpd.app.run_server(debug=True, port=8051)
