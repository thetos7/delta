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


        self.data_count = data_count
        self.data_watchtime = data_watchtime

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de décès par jour en France'),
            html.Div([dcc.Graph(id='mpj-main-graph'), ], style={'width': '100%', }),
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

            Notes :
               * On met nos notes

            #### À propos

            * Sources : 
                https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114045/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-nombre-de-sujets.csv
                https://static.data.gouv.fr/resources/classement-thematique-des-sujets-de-journaux-televises-janvier-2005-septembre-2020/20201202-114231/ina-barometre-jt-tv-donnees-mensuelles-2005-2020-durees.csv

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

    def update_graph(self, mean):
        fig = px.line(self.df, template='plotly_white')
        fig.update_traces(hovertemplate='%{y} décès le %{x:%d/%m/%y}', name='')
        fig.update_layout(
            # title = 'Évolution des prix de différentes énergies',
            xaxis=dict(title=""),  # , range=['2010', '2021']),
            yaxis=dict(title="Nombre de décès par jour"),
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
    mpj = TvSubject()
    mpj.app.run_server(debug=True, port=8051)
