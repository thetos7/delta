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

        df_tdp = pd.read_csv('./presidentielle/data/temps_de_parole_presidentielles_2022.csv')
        print(pd.unique(df_tdp['Candidat']))
        print(pd.unique(df_tdp['Période']))
        # self.df_sondage_t2 = df
        # self.day_mean = prediction
        # '2022-04-08'
        fig_tdp_t1 = px.bar(df_tdp[df_tdp['Période'] == '2022-03-27'], x='Candidat', y="Somme",
                            color='Chaîne', barmode="group", labels={
                "Période": "Temps en jours",
                "Somme": "Temps de parole en minutes",
                "Chaîne": "Chaîne"
            }, title="Temps de parole pour fache candidats en fonction des médias")

        fig_tdp_t2 = px.bar(df_tdp[(df_tdp['Période'] == '2022-04-08') & (
                (df_tdp['Candidat'] == 'Macron') | (df_tdp['Candidat'] == 'Lepen'))], x='Candidat', y="Somme",
                            color='Chaîne', barmode="group", labels={
                "Période": "Temps en jours",
                "Somme": "Temps de parole en minutes",
                "Chaîne": "Chaîne"
            }, title="Temps de parole pour fache candidats en fonction des médias")

        self.main_layout = html.Div(children=[
            html.H2(children='Sondages présidentiels et temps de parole dans les médias'),
            html.H3(children='Premier tour'),
            html.Div(
                [dcc.Graph(id='sond_t1', figure=fig_sond_t1)], style={'width': '100%', }),
            dcc.Markdown("""
             ##### Notes :
             - L'arrivée de certains candidats fait perdre des voix à certains qu'ils ne regagneront jamais même 
             si le candidat n'est se retire de la présidentielle (Mme Taubira et M. Jadot)
             - Mme Le Pen et M. Mélenchon sont monté dans les sondages sur les 2 dernières semaines et ont fait 
             perdre des voix aux autres candidats
            """),
            html.Div(
                [dcc.Graph(id='dtp_t1', figure=fig_tdp_t1)], style={'width': '100%', }),
            dcc.Markdown(""" 
            ##### Notes :
            - Certains médias parlent beaucoup plus des élections présidentielles que d'autres
            - Le temps de parole totale des candidats dans les médias ne reflète pas leur passage ou non au second tour 
            (Mme Le Pen a passé beaucoup moins de temps dans les médias que Mme Pecresse et a pourtant accédé au second tour)
            - 
            """),
            html.H3(children='Second tour'),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig_sond_t2)], style={'width': '100%', }),
            dcc.Markdown("""
             ##### Notes :
             - Les sondages datant d'avant le second tour sont les sondages qui représentent les 
             intentions de vote opposants Mme Le Pen et M. Macron
             - Mme Le Pen et M. Macron ont toujours été très proches au niveau des sondages
             - Sur la période du second tour et en prenant en comptent les erreurs de sondages 
             Mme Le Pen est passé devant M. Macron plusieurs fois
            """),
            html.Div(
                [dcc.Graph(id='dtp_t2', figure=fig_tdp_t2)], style={'width': '100%'}),
            dcc.Markdown("""
             ##### Notes :
             - Les deux candidats du second tour n'ont pas été représentés équitablement durant la période de l'entre-deux tours.
             - Certains médias représentent plus M. Macron et d'autres Mme. Le Pen
            """),
            html.Br(),
            html.H3(children='À propos'),
            dcc.Markdown(""" 
                        * Données sondage: [Nsppolls](https://github.com/nsppolls/nsppolls/blob/master/presidentielle.csv)
                        * Données temps de parole : [CSA](https://www.csa.fr/Proteger/Garantie-des-droits-et-libertes/Proteger-le-pluralisme-politique/La-presidentielle-2022)
                        * (c) 2022 Guillaume Larue et Enguerrand de Gentile Duquesne
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
