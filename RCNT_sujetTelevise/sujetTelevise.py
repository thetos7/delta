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



class TvSubject():
    def __init__(self, application=None):

        # # # # # # # # # # # # # # #
        # Download data             #
        # # # # # # # # # # # # # # #

        column_names = ['MOIS', 'THEMATIQUES', 'TF1', 'France 2', 'France 3', 'Canal +', 'Arte', 'M6', 'TOTAUX']

        data_watchtime = pd.read_csv('data/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv', sep=";",
                                     skipinitialspace=True,
                                     quotechar="'", header=0, skiprows=1, names=column_names, encoding='latin-1',
                                     parse_dates=[1])
        data_count = pd.read_csv('data/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv', sep=";",
                                 skipinitialspace=True,
                                 quotechar="'", header=0, skiprows=1, names=column_names, encoding='iso8859_15',
                                 parse_dates=[1])
        # # # # # # # # # # # # # # #
        # Data Cleaning             #
        # # # # # # # # # # # # # # #

        # # # # # # # # # # # # # # # #
        # Change the date to datetime #
        # # # # # # # # # # # # # # # #
        def month_to_number(months):
            if months == 'janvier':
                return "01"
            elif months[0] == 'f':
                return "02"
            elif months == 'mars':
                return "03"
            elif months == 'avril':
                return "04"
            elif months == 'mai':
                return "05"
            elif months == 'juin':
                return "06"
            elif months[0] == 'j':
                return "07"
            elif months[0] == 'a':
                return "08"
            elif months[0] == 's':
                return "09"
            elif months[0] == 'o':
                return "10"
            elif months[0] == 'n':
                return "11"
            elif months[0] == 'd':
                return "12"
            return "ERROR"

        def string_to_date_time(date):
            L = date.split("-")
            L[1] = "20" + L[1]
            L = L[1] + "-" + month_to_number(L[0])
            return L

        data_count["MOIS"] = data_count["MOIS"].apply(lambda date: string_to_date_time(date))
        data_watchtime["MOIS"] = data_watchtime["MOIS"].apply(lambda date: string_to_date_time(date))

        # # # # # # # # # # # # # # #
        # CLean Data Accent         #
        # # # # # # # # # # # # # # #

        def clean_accent(string):
            if (string.startswith("Sant")):
                string = "Sante"
            if (string.startswith("Soci")):
                string = "Societe"
            return string

        data_watchtime["THEMATIQUES"] = data_watchtime["THEMATIQUES"].apply(lambda string: clean_accent(string))
        data_count["THEMATIQUES"] = data_count["THEMATIQUES"].apply(lambda string: clean_accent(string))

        # # # # # # # # # # # # # # #
        # CLean Column type         #
        # # # # # # # # # # # # # # #
        # clean count df

        data_count["MOIS"] = data_count["MOIS"].apply(pd.to_datetime)
        data_count[["TF1", "France 2", "France 3", "Canal +", "Arte", "M6", "TOTAUX"]] = data_count[
            ["TF1", "France 2", "France 3", "Canal +", "Arte", "M6", "TOTAUX"]].apply(pd.to_numeric)

        # clean watchtime df
        data_watchtime["MOIS"] = data_watchtime["MOIS"].apply(pd.to_datetime)
        for col in data_watchtime.columns[2:]:
            data_watchtime[col] = pd.to_timedelta(data_watchtime[col]) / pd.Timedelta('1s')
            data_watchtime[col] = data_watchtime[col].apply(int)
        data_watchtime = data_watchtime.set_index("MOIS")


        # # # # # # # # # # # # # # # # # # #
        # Other table due to multi-index    #
        # # # # # # # # # # # # # # # # # # #
        thematiques_names = ["Catastrophes", "Culture-loisirs", "Economie", "Education", "Environnement",
                             "Faits divers", "Histoire-hommages", "International", "Justice", "Politique France",
                             "Sante", "Sciences et techniques", "Societe", "Sport"]

        data_watchtime_tot = data_watchtime.drop(["TF1", "France 2", "France 3", "Canal +", "Arte", "M6"], axis=1)
        for i in thematiques_names:
            data_watchtime_tot[i] = data_watchtime_tot[data_watchtime_tot["THEMATIQUES"] == i]["TOTAUX"]
        data_watchtime_tot = data_watchtime_tot.drop(["THEMATIQUES", "TOTAUX"], axis=1).drop_duplicates()

        data_count_ind = data_count.set_index("MOIS")
        data_count_tot = data_count_ind.drop(["TF1", "France 2", "France 3", "Canal +", "Arte", "M6"], axis=1)
        for i in thematiques_names:
            data_count_tot[i] = data_count_tot[data_count_tot["THEMATIQUES"] == i]["TOTAUX"]
        data_count_tot = data_count_tot.drop(["THEMATIQUES", "TOTAUX"], axis=1).drop_duplicates()


        self.data_count = data_count
        self.data_watchtime = data_watchtime

        self.data_count_tot = data_count_tot
        self.data_watchtime_tot = data_watchtime_tot

        self.main_layout = html.Div(children=[
            html.H3(children='Quelques statistiques sur le sujet télévisées'),
            html.Div([dcc.Graph(id='mpj-main-graph'), ], style={'width': '100%', }),
            html.Div([dcc.RadioItems(id='mpj-mean',
                                     options=[{'label': 'Courbe en fonction des chaines TV', 'value': 0},
                                              {'label': 'Courbe + Tendence générale', 'value': 1},
                                              {
                                                  'label': 'Courbe + Moyenne journalière (les décalages au 1er janv. indique la tendence)',
                                                  'value': 2},
                                              {'label': 'Courbe + Tendence générale', 'value': 3}],
                                     value=0,
                                     labelStyle={'display': 'block'}),
                      ]),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la courbe, réinitialiser.

            Notes :
               * On met nos notes

            #### À propos

            * Sources : 
                * https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv
                * https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114231/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv

            * 2022 Romain Cazin, Nicolas Trabet
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

        self.app.callback(
            dash.dependencies.Output('mpj-main-graph', 'figure'),
            dash.dependencies.Input('mpj-mean', 'value'))(self.update_graph)

    def update_graph(self, mean = 0):
        themes = self.data_watchtime.groupby('THEMATIQUES').sum() / 3600  # en heure
        if mean == 0:
            fig = px.line(self.data_watchtime[self.data_watchtime["THEMATIQUES"] == "Education"].drop(["THEMATIQUES"], axis=1))
            fig.update_layout(
                title='time',
                yaxis=dict(title='in sec')
            )


        elif mean == 1:
            fig = px.line(self.data_watchtime_tot)
            fig.update_layout(
                title='time',
                yaxis=dict(title='in sec')
            )

        elif mean == 2:
            graph = (self.data_watchtime.drop(["THEMATIQUES"], axis=1) / self.data_count.set_index("MOIS").drop(["THEMATIQUES"], axis=1)).mean()
            layout_histo = dict(
                title='Average time for french tv news programs depending on the Channel between 2005 to 2020',
                xaxis=dict(title='Themes'),
                yaxis=dict(title='How many time (in sec)'),
            )
            fig = px.bar(graph)
            fig.update_layout(layout_histo)
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

        elif mean == 3:
            graph = (self.data_watchtime_tot / self.data_count_tot).mean()
            layout_histo = dict(
                title='Average time for french tv news programs depending on the subject between 2005 to 2020',
                xaxis=dict(title='Themes'),
                yaxis=dict(title='How many time (in sec)'),
            )
            fig = px.bar(graph)
            fig.update_layout(layout_histo)
            fig.update_layout(xaxis={'categoryorder': 'total descending'})

        return fig


if __name__ == '__main__':
    mpj = TvSubject()
    mpj.app.run_server(debug=True, port=8051)
