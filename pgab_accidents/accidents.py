from typing import Union
import glob
import dash
from dash import html
import dash_core_components as dcc
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# TODO create layout
class Accidents:
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = pd.concat([pd.read_pickle(f) for f in glob.glob('data/acc_caracs_grav-*')]).sort_values('year')

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des accidents de la route en France métropolitaine entre 2005 et 2020'),
            html.Div([ dcc.Graph(id='acc-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='acc-type', 
                                     options=[{'label':'Heatmap', 'value':0},
                                              {'label':'Emplacements exacts', 'value':1}], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            dcc.Markdown("""
            Carte intéractive des accidents de la route entre 2016 et 2020. Utilisez le slider afin de sélectionner l'année.
            La carte comporte plusieurs calques:
            * Heatmap des accidents
            * Emplacements exacts

            #### À propos
            * Données: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/)

            &copy; 2022 Paul Galand & Ancelin Bouchet
            """, style={'margin-top': '3rem'})
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
            'display': 'flex',
            'flex-direction': 'column'
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('acc-main-graph', 'figure'),
                    dash.dependencies.Input('acc-type', 'value'))(self.update_graph)

    def update_graph(self, acc_type):
        if acc_type:
            fig=px.scatter_mapbox(self.df, lat='lat', animation_frame="year",
                                  lon='long', color='grav', mapbox_style='carto-positron',
                                  zoom=4, center=dict(lat=46.7111, lon=1.7191))
        else:
            fig=px.density_mapbox(self.df, z=None, lat='lat', animation_frame="year",
                                  lon='long', radius=5, opacity=.6, mapbox_style='carto-positron',
                                  zoom=4, center=dict(lat=46.7111, lon=1.7191),
                                  color_continuous_scale=px.colors.diverging.Picnic)
            fig.update_layout(coloraxis_showscale=False)
        fig.update_traces(hovertemplate="Date: %{jour} %{mois} %{year}\nGravité: %{grav}", name="year")

        return fig
#         if mean == 1:
#             reg = stats.linregress(np.arange(len(self.df)), self.df.morts)
#             fig.add_scatter(x=[self.df.index[0], self.df.index[-1]], y=[reg.intercept, reg.intercept + reg.slope * (len(self.df)-1)], mode='lines', marker={'color':'red'})
#         elif mean == 2:
#             fig.add_scatter(x=self.df.index, y=self.day_mean, mode='lines', marker={'color':'red'})
        
    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    acc = Accidents()
    acc.run(port=8065)
