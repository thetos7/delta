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

        # Nomenclature utilisée par l'INSEE
        self.nomenclature_INSEE = [["A", "Agriculture, sylviculture et pêche"], ["B", "Industries extractives"],
                            ["C", "Industrie manufacturière"],
                            ["D", "Production et distribution d'électricité, de gaz, de vapeur et d'air conditionné"],
                            ["E", "Production et distribution d'eau ; assainissement, gestion des déchets et dépollution"],
                            ["F", "Construction"], ["G", "Commerce ; réparation d'automobiles et de motocycles"],
                            ["H", "Transports et entreposage"], ["I", "Hébergement et restauration"],
                            ["J", "Information et communication"], ["K", "Activités financières et d'assurance"],
                            ["L", "Activités immobilières"], ["M", "Activités spécialisées, scientifiques et techniques"],
                            ["N", "Activités de services administratifs et de soutien"], ["O", "Administration publique"],
                            ["P", "Enseignement"], ["Q", "Santé humaine et action sociale"],
                            ["R", "Arts, spectacles et activités récréatives"], ["S", "Autres activités de services"],
                            ["T", "Activités des ménages en tant qu'employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre"],
                            ["U", "Activités extra-territoriales"], ["X", "Inconnu"]]

        # dictionnaires permettant la convertion de la nomenclature utilisée par l'INSEE
        self.INSEE_to_secteur = {insee: secteur for insee, secteur in self.nomenclature_INSEE}
        self.secteur_to_INSEE = {secteur: insee for insee, secteur in self.nomenclature_INSEE}

        self.insee = pd.DataFrame.from_dict({"Nomenclature de l'INSEE": [nomenclature for nomenclature, _ in self.INSEE_to_secteur.items()], "Secteur d'activité": [activite for _, activite in self.INSEE_to_secteur.items()]}).transpose()
        self.dpo = pd.read_pickle('tpmm_RGPD/data/1_data_dpo.pkl')
        self.notification = pd.read_pickle('tpmm_RGPD/data/1_data_notification.pkl')
        self.budget_cnil_sanctions = pd.read_pickle('tpmm_RGPD/data/2_budget_cnil_sanctions.pkl')
        self.sanc_avert_mise_en_demeure_controles = pd.read_pickle('tpmm_RGPD/data/3_sanc_avert_mise_en_demeure_controles.pkl')

        self.main_layout = html.Div(children=[
            html.H3(children="Évolution de l'application du RGPD en France"),
            html.H4(children="Authors: Marc Monteil et Théo Perinet"),

            html.Div([ dcc.Graph(figure=self.update_1_insee())], style={'width':'100%', }),
            html.Div([ dcc.Graph(id='rgpd-1-donnees'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Type d\'informations'),
                           dcc.Dropdown(
                               id='rgpd-1-which-info',
                               options=[{'label': i, 'value': i} for i in ['DPOs', 'Notifications']],
                               value="DPOs"
                           ),
                         ], style={'width': '12em'}),
                html.Div(style={'width':'2em'}),
                html.Div([ html.Div('Mode d\'affichage'),
                           dcc.Dropdown(
                               id='rgpd-1-which-mode',
                               options=[{'label': i, 'value': i} for i in ['Données brut', 'Somme cumulée']],
                               value='Somme cumulée'
                           ),
                         ], style={'width': '12em'} )
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
    
    def update_1_insee(self):
        fig = go.Figure(data=[go.Table(
                    columnwidth = [80, 400],
                    header=dict(values=list(self.insee.index),
                    align='left'),
                cells=dict(values=self.insee,
                    fill_color='lavender',
                    align='left'))
                    ])
        fig.update_layout(
            title = "Correspondance entre la nomenclature de l'INSEE et le secteure d'activité",
        )
        return fig

    def update_1_info_graph(self, info, mode):
        if info == None or info == "DPOs":
            df = self.dpo.copy()
            cur_ytitle = "Nombre de DPO enregistrés"
        else:
            df = self.notification.copy()
            cur_ytitle = "Nombre de notifications envoyées"

        if mode == None or mode == 'Somme cumulée':
            df = df.cumsum()
        else:
            cur_ytitle += " durant le mois"

        fig = px.bar(df)

        for c in df.columns:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=self.INSEE_to_secteur[c], hoverinfo='x+y+text')

        fig.update_layout(
            title = "Nombre de DPO enregistrés / notifications envoyées",
            yaxis = dict( title = cur_ytitle),
            xaxis = dict( title = "Date"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Secteur d\'activité'},
        )
        return fig


if __name__ == '__main__':
    rgpd = RGPD()
    rgpd.app.run_server(debug=True, port=8051)
