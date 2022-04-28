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
import datetime

class CovidBasics():
    def __init__(self, application = None):
        self.df = pd.read_pickle('data/covid-all-stats-departments.pkl')

        self.main_layout = html.Div(children=[
            html.H3(children='Covid Basics'),
            html.Div([ dcc.Graph(figure=self.update_graph()), ], style={'width':'100%', }),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.

            Sources : https://www.data.gouv.fr/fr/datasets/synthese-des-indicateurs-de-suivi-de-lepidemie-covid-19/
            
            Notes :
               * On observe qu'il n'y avait pas de recensement au début de l'épidémie.
               * On peut notamment voir les deux pics de cas, Octobre-Novembre 2020, amenant au 2nd confinement, et Janvier 2022.
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

        # self.app.callback(dash.dependencies.Output('cvd-main-graph', 'figure'))(self.update_graph)

    def update_graph(self):
        fig = px.line(
          self.df,
          template='plotly_white',
          x=self.df.index.get_level_values(0),
          y="pos"
        )

        # fig.update_traces(hovertemplate='%{y} décès le %{x:%d/%m/%y}', name='')
        # fig.update_layout(
        #     #title = 'Évolution des prix de différentes énergies',
        #     xaxis = dict(title=""), # , range=['2010', '2021']), 
        #     yaxis = dict(title="Nombre de décès par jour"), 
        #     height=450,
        #     showlegend=False,
        # )
       
        return fig

        
if __name__ == '__main__':
    cvd = CovidBasics()
    cvd.app.run_server(debug=True, port=8051)
