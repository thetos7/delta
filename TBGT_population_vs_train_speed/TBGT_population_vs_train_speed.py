#!/usr/bin/env python3

from dash import dcc, html

from .get_data import get_train_data


class TBGT:
    def __init__(self, application = None):
        self.train_df = get_train_data()
        self.main_layout = html.Div(children=[
            html.H3(children='Évolution de la population par rapport au développement des grandes lignes en France'),
            dcc.RadioItems(list(self.train_df.groups.keys()), style={'font-size': '10px'})
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })
