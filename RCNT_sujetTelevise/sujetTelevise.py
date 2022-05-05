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
        df = pd.concat([pd.read_pickle(f) for f in glob.glob('data/morts_par_jour-*')])
        df = df.groupby('deces').sum()
        df.sort_index(inplace=True)
        last_month = "02/2022"
        now = np.datetime64(datetime.datetime.now()).astype('datetime64[M]')
        df = df.loc['1973':now - np.timedelta64(2, 'M')]

        # calcul de la moyenne journalière avec des fenêtres
        # 2 passages pour retirer les valeurs qui dépassent l'écart type par rapport au sinus
        width = 10
        df2 = df.copy()
        for _ in range(2):
            prediction = pd.DataFrame({'x': np.zeros(len(df))}, index=df.index)
            prediction_nb = pd.DataFrame({'x': np.zeros(len(df))}, index=df.index)
            for step in range(1970, df.index[-1].year - width + 1):
                dfp = df2.loc[f'{step}':f'{step + width}']
                pente, v0 = np.polyfit(np.arange(len(dfp)), dfp.morts.values, 1)
                y = fft.fft(dfp.morts)
                y[y < 30 * len(dfp)] = 0
                pred = fft.ifft(y)
                pred -= dfp.morts.mean() - v0
                pred += np.cumsum([pente, ] * len(dfp))
                prediction.loc[f'{step}':f'{step + width}', 'x'] += pred
                prediction_nb.loc[f'{step}':f'{step + width}', 'x'] += 1
            prediction = np.array([p.real for p in prediction.x]) / prediction_nb.x
            std = np.std(df.morts - prediction)
            df2.morts[df2.morts > prediction + std] = prediction.astype('int') + int(std)
            df2.morts[df2.morts < prediction - std] = prediction.astype('int') - int(std)
        del df2

        self.df = df
        self.day_mean = prediction

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

            * Sources : https://www.data.gouv.fr/fr/datasets/fichier-des-personnes-decedees/
            * (c) 2022 Olivier Ricou
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
    mpj = Deces()
    mpj.app.run_server(debug=True, port=8051)
