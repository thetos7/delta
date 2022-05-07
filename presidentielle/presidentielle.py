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


class Presidentielles():
    def __init__(self, application=None):
        df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')
        df.drop(['id', 'echantillon', 'erreur_sup', 'sous_echantillon', 'commanditaire',
                 'erreur_inf', 'population', 'rolling', 'media', 'parti'], axis=1, inplace=True)
        df = df[df['nom_institut'] == 'Ipsos']
        df["hypothese"].replace(np.nan, "tous", inplace=True)
        df = df[(df['hypothese'] == "tous") & (df['tour'] == "Premier tour")]
        df.reset_index()
        df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
        df = df[df['tour'] == "Premier tour"]
        df = df.sort_values(by="date_enquete")

        fig_sond_t1 = px.line(df, y="intentions", x="date_enquete", color="candidat",
                              title='Sondage en vu du premier tous des présidentielles par candidat')

        self.df_sondage_t1 = df

        df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')

        df.drop(['parti', 'id', 'commanditaire', 'debut_enquete', 'population', 'rolling', 'media', 'sous_echantillon'],
                axis=1, inplace=True)
        df = df[df['tour'] == "Deuxième tour"]
        df.replace("Hypothèse Macron", "Hypothèse Macron / Le Pen", inplace=True)
        df.replace("Hypothèse Le Pen / Macron", "Hypothèse Macron / Le Pen", inplace=True)
        df.replace(np.nan, "Hypothèse Macron / Le Pen", inplace=True)
        df.reset_index(inplace=True)
        df = df[df["hypothese"] == "Hypothèse Macron / Le Pen"]
        df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
        df_ifop = df[df['nom_institut'] == 'Ifop']
        df_ifop = df_ifop.sort_values(by="date_enquete")

        fig_sond_t2 = px.line(df_ifop, x="date_enquete", y="intentions", color="candidat",
                              title='Sondage des en vu du dexième tour des présidentielles par candidat')
        # px.line(df_ifop, x="date_enquete", y="erreur_sup", color="candidat")

        self.df_sondage_t2 = df
        # self.day_mean = prediction

        self.main_layout = html.Div(children=[
            html.H3(children='Sondages présidentiels et temps de parole dans les médias'),
            html.Div(
                [dcc.Graph(id='sond_t1', figure=fig_sond_t1)
                    , dcc.Graph(id='sond_t2', figure=fig_sond_t2)], style={'width': '100%', }),
            html.Div([dcc.RadioItems(id='mpj-mean',
                                     options=[{'label': 'Courbe seule', 'value': 0},
                                              {'label': 'Courbe + Tendence générale', 'value': 1},
                                              {
                                                  'label': 'Courbe + Moyenne journalière (les décalages au 1er janv. indique la tendence)',
                                                  'value': 2}],
                                     value=2,
                                     labelStyle={'display': 'block'}),
                      ]),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.

            Sources : https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv

            Notes :
               * test
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
        """
        self.app.callback(
            dash.dependencies.Output('mpj-main-graph', 'figure'),
            dash.dependencies.Input('mpj-mean', 'value'))(self.update_graph)
        """

    def update_graph(self, mean):
        fig = px.line(self.df, template='plotly_white')
        fig.update_traces(hovertemplate='%{y} décès le %{x:%d/%m/%y}', name='')
        fig.update_layout(
            # title = 'Évolution des prix de différentes énergies',
            xaxis=dict(title=""),  # , range=['2010', '2021']),
            yaxis=dict(title="Sondage présidentiels"),
            height=450,
            showlegend=False,
        )
        if mean == 1:
            reg = stats.linregress(np.arange(len(self.df)), self.df.morts)
            fig.add_scatter(x=[self.df.index[0], self.df.index[-1]],
                            y=[reg.intercept, reg.intercept + reg.slope * (len(self.df) - 1)], mode='lines',
                            marker={'color': 'red'})
        elif mean == 2:
            fig.add_scatter(x=self.df.index, y=self.day_mean, mode='lines', marker={'color': 'red'})

        return fig


if __name__ == '__main__':
    mpj = Presidentielles()
    mpj.app.run_server(debug=True, port=8051)
