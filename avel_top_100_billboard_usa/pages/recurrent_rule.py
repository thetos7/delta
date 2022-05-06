import sys
import dash
import flask
from dash import dcc
from dash import html, Dash, Output, Input, dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

dash.register_page(__name__, path='/recurrent_rule')


def layout():
    layout = html.Div([
        html.H1('Top 100 Billboard USA'),

        html.H3('Informations à propos des données'),
        dcc.Markdown(f'''
            
            Il s'agit d'un tableau des classements de la Billboard Hebdomadaire des USA de 1958 à 2021,   
            comprenant {len(self.df)} entrées dont {self.song_count} chansons et {self.artist_count} artistes uniques.
            
            
            '''),

        html.H3('Notes'),
        dcc.Markdown('''
            ### Sources   
            https://www.billboard.com/billboard-charts-legend/
            '''),

    ])
    return layout
