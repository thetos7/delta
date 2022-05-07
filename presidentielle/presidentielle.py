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
import os

class Presidentielles():
    def __init__(self, application=None):
        cwd = os.getcwd()
        print(cwd)

        df = pd.read_csv('./presidentielle/data/sondages_tour_1.csv')

        fig_sond_t1 = px.line(df, y="intentions", x="date_enquete", color="candidat",
                              title='Sondage en vu du premier tous des présidentielles par candidat')

        self.df_sondage_t1 = df

        df = pd.read_csv('./presidentielle/data/sondages_tour_2.csv')

        df_lepen = df[df["candidat"] == "Marine Le Pen"]
        df_macron = df[df["candidat"] == "Emmanuel Macron"]

        fig_sond_t2 = go.Figure()
        fig_sond_t2.add_trace(go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["intentions"], name="Marine Le Pen",
                                         line=dict(color='royalblue', width=2)))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["erreur_sup"], name="Erreur Sup : Marine Le Pen",
                       line=dict(color='royalblue', width=2, dash='dash')))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_lepen["date_enquete"], y=df_lepen["erreur_inf"], name="Erreur Inf : Marine Le Pen",
                       line=dict(color='royalblue', width=2, dash='dot')))

        fig_sond_t2.add_trace(go.Scatter(x=df_macron["date_enquete"], y=df_macron["intentions"], name="Emmanuel Macron",
                                         line=dict(color='firebrick', width=2)))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_macron["date_enquete"], y=df_macron["erreur_sup"], name="Erreur Sup : Emmanuel Macron",
                       line=dict(color='firebrick', width=2, dash='dash')))
        fig_sond_t2.add_trace(
            go.Scatter(x=df_macron["date_enquete"], y=df_macron["erreur_inf"], name="Erreur Inf : Emmanuel Macron",
                       line=dict(color='firebrick', width=2, dash='dot')))

        fig_sond_t2.update_layout(title='Sondages présidentiels du second tour avec prise en compte de l\'erreur',
                                  xaxis_title='Temps',
                                  yaxis_title='Pourcentage de vote')

        # fig_tdp =

        self.df_sondage_t2 = df
        # self.day_mean = prediction

        self.main_layout = html.Div(children=[
            html.H2(children='Sondages présidentiels et temps de parole dans les médias'),
            html.H3(children='Premier tour'),
            html.Div(
                [dcc.Graph(id='sond_t1', figure=fig_sond_t1)], style={'width': '100%', }),
            html.Div([dcc.RadioItems(id='mpj-mean',
                                     options=[{'label': 'Courbe seule', 'value': 0},
                                              {'label': 'Courbe + Tendence générale', 'value': 1},
                                              {
                                                  'label': 'Courbe + Moyenne journalière (les décalages au 1er janv. indique la tendence)',
                                                  'value': 2}],
                                     value=2,
                                     labelStyle={'display': 'block'}),
                      ]),
            html.H3(children='Second tour'),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig_sond_t2)], style={'width': '100%', }),

            html.Br(),
            html.H3(children='À propos'),
            dcc.Markdown(""" 
                        * Données : [Nsppolls](https://github.com/nsppolls/nsppolls/blob/master/presidentielle.csv)
                        * (c) 2022 Guillaume LARUE et Enguerrand de Gentile Duquesne
                        """),
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
