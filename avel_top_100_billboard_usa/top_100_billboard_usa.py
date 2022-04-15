import sys
import dash
import flask
from dash import dcc
from dash import html, Dash, Output, Input
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du


class Top100BillboardUSA:
    def __init__(self, application: Dash = None):
        # Importing the data
        self.df = pd.read_csv('data/top_100_billboard_usa.csv')

        # Creating the Dash application
        self.app = Dash(__name__) if application is None else application
        self.app.layout = self.get_app_layout()
        self.callbacks()

    def get_app_layout(self) -> html.Div:
        """
        Returns the default layout for the Dash application.
        :return: html.Div
        """
        layout = html.Div([
            html.H1('Top 100 Billboard USA'),
            html.Div([
                "Input: ",
                dcc.Input(id='my-input', value='', type='text')
            ]),
            html.Table(id='foo'),

        ])
        return layout

    @staticmethod
    def generate_table(dataframe: pd.DataFrame, max_rows: int = 10) -> html.Table:
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ])

    def callbacks(self) -> None:
        # Example callback
        @self.app.callback(Output("foo", "children"), Input('my-input', 'value'))
        def update_graph(input_value):
            return html.Div([
                html.H2(input_value),
                self.generate_table(self.df),
            ])


if __name__ == '__main__':
    nrg = Top100BillboardUSA()
    nrg.app.run_server(debug=True)
