import pandas as pd
from dash import dcc, html, Input, Output, dash
import plotly.express as px


def update_bar_chart(dims):
    df = px.data.iris()  # replace with your own data source
    fig = px.scatter_matrix(
        df, dimensions=dims, color="species")
    return fig


class Formations:

    def __init__(self, application=None):
        self.main_layout = None
        df = px.data.gapminder().query("year == 2007")
        fig = px.treemap(df, path=[px.Constant('world'), 'continent', 'country'], values='pop',
                         color='lifeExp', hover_data=['iso_alpha'])
        self.main_layout = html.Div([
            dcc.Graph(figure=fig)
        ])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            Output("graph", "figure"),
            Input("dropdown", "value"))(update_bar_chart)
