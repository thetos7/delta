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


class Independance_Petrole():
    def __init__(self, application=None):
        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""Independance Européene face au Petrole comme energie fossile""")
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
    pol = Independance_Petrole()
    pol.app.run_server(debug=True, port=8051)
