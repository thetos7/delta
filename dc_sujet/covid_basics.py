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

            Sources : https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/
            
            Notes :
               * La grippe de l'hiver 1989-1990 a fait 20 000 morts (4,6 millions de malades en 11 semaines). La chute de la courbe au premier janvier 1990 est quand même très surprenante.
               * On repère bien les hivers avec grippe.
               * L'année 1997 est étrange, peut-être un problème de recensement.
               * La canicule d'août 2003 a fait 15 000 morts (ce qui a généré la journée de travail non payé dite journée Raffarin).
               * Les 120 000 morts dus au Covid-19 en 2020 et 2021 sont bien visibles, d'autant qu'il n'y a pas eu de grippe durant les hivers 19-20 et 20-21.
               * On note une progression constante du nombre de morts, avec environ 1000 morts par jour en dehors de pics durant les années 70 
                 pour environ 1700 morts par jour après 2015. Il s'agit d'une augmentation de plus de 70 %, soit plus du double que l'augmentation de la population sur la même période. Le saut visible en 1990 peut aussi traduire un recensement plus complet après cette année.
               * Les derniers mois doivent être pris avec précaution car tous les morts ne sont pas encore recensés.
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
