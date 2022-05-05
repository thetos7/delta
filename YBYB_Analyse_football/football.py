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

class Football():

    def __init__(self, application = None):

        pd.options.plotting.backend = "plotly"

        leagues = pd.read_csv("YBYB_Analyse_football/data/concat_leagues/leagues.csv")

        league_colors = {'liga':'gold', 'PL':'blue', 'serieA':'green', 'ligue1':'black', 'bundesliga':'red'}

        fig = px.scatter(leagues, x='Rk', y='Age', color="league", hover_name="Squad", 
                color_discrete_map=league_colors, title="Déplacez la souris sur une bulle pour avoir les graphiques du club en bas.",
                size = 'Market Value', 
                size_max=60, 
                animation_frame=leagues["Years"], animation_group="Squad", range_y=[leagues['Age'].min(), leagues['Age'].max()], range_x=[1,20])
                
        self.main_layout = html.Div(children=[
            html.H3(children='Classement en fonction de l age et de la valeur marchande des clubs'),
            html.Div([ dcc.Graph(figure=fig), ], style={'width':'100%', }),  
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
    foot = Football()
    foot.app.run_server(debug=True, port=8051)
