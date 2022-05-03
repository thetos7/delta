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

class RGPD():

    def __init__(self, application = None):
        self.dpo = pd.read_pickle('data/1_data_dpo.pkl')
        self.notification = pd.read_pickle('data/1_data_notification.pkl')
        self.budget_cnil_sanctions = pd.read_pickle('data/2_budget_cnil_sanctions.pkl')
        self.sanc_avert_mise_en_demeure_controles = pd.read_pickle('data/3_sanc_avert_mise_en_demeure_controles.pkl')

        self.main_layout = html.Div(children=[
            html.H3(children="Évolution de l'application du RGPD en France"),
            html.H4(children="Authors: Marc Monteil et Théo Perinet"),

            html.Div([ dcc.Graph(id='rgpd-1-donnees'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Type d\'informations'),
                           dcc.Dropdown(
                               id='rgpd-1-which-info',
                               options=[{'label': i, 'value': i} for i in ['DPOs', 'Notifications']],
                               value="DPOs"
                           ),
                         ], style={'width': '8em'}),
                html.Div([ html.Div('Mode d\'affichage'),
                           dcc.Dropdown(
                               id='rgpd-1-which-mode',
                               options=[{'label': i, 'value': i} for i in ['Données brut', 'Somme cumulée']],
                               value='Somme cumulée'
                           ),
                         ], style={'width': '8em', 'padding':'2em 0px 0px 0px'} )
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

            html.Br(),
            dcc.Markdown("""
            #### À propos

            * Sources : 
                * [base Pégase](http://developpement-durable.bsocom.fr/Statistiques/) du ministère du développement durable
                * [tarifs réglementés de l'électricité](https://www.data.gouv.fr/en/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/) sur data.gouv.fr
            * (c) 2022 Théo Perinet et Marc Monteil
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
                    dash.dependencies.Output('rgpd-1-donnees', 'figure'),
                    [ dash.dependencies.Input('rgpd-1-which-info', 'value'),
                      dash.dependencies.Input('rgpd-1-which-mode', 'value')])(self.update_1_info_graph)
    
    def update_1_info_graph(self, info, mode):
        if info == None or info == "DPOs":
            df = self.dpo.copy()
            cur_title = "Nombre de DPO enregistrés"
        else:
            df = self.notification.copy()
            cur_title = "Nombre de notifications envoyées"

        if mode == None or mode == 'Somme cumulée':
            df = df.cumsum()
        else:
            cur_title += " durant le mois"

        fig = px.bar(df)

        fig.update_layout(
            title = cur_title,
            yaxis = dict( title = "Nombre"),
            xaxis = dict( title = "Date"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Secteur d\'activité'},
        )
        return fig


if __name__ == '__main__':
    rgpd = RGPD()
    rgpd.app.run_server(debug=True, port=8051)
