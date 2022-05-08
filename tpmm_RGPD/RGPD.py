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

            html.Br(),
            html.Br(),

            dcc.Markdown("""Le règlement général sur la protection des données (RGPD, ou encore GDPR en anglais), est un règlement de l'Union européenne qui constitue le texte de référence en matière de protection des données à caractère personnel. 
            Il renforce et unifie la protection des données pour les individus au sein de l'Union européenne.
            Ce règlement a été définitivement adopté par le Parlement européen le 27 avril 2016. 
            Ses dispositions sont directement applicables dans l'ensemble des 27 États membres de l'Union européenne à compter du 25 mai 2018. 
            Source : https://fr.wikipedia.org/wiki/R%C3%A8glement_g%C3%A9n%C3%A9ral_sur_la_protection_des_donn%C3%A9"""),
            html.Br(),
            
            dcc.Markdown("""Dans ce projet, nous allons voir dans quel mesure le RGPD a été appliqué en France depuis que la loi a été votée à travers la variation du nombre de DPO (Data Protection Officer) dans les entreprises,
            ainsi que le nombre de notification que ceux ci ont envoyés à la CNIL (Commission Nationale de l'Informatique et de Libertés), qui s'occupe des contrôle relatifs au RGPD.
            Nous allons également étudier l'évolution de la CNIL, de son budget et de ses actions."""),
            html.Br(),
            
            html.H4(children="Évolution du nombre de notifications et DPOs"),
            dcc.Markdown("""Le data frame suivant montre la correspondance entre la nomenclature de l'INSEE et le secteur d'activité.
            Les nomenclatures d'activités ont été élaborées principalement en vue de faciliter l'organisation de l'information économique et sociale. 
            Leur finalité est donc essentiellement statistique et d'ailleurs les critères d'ordre juridique ou institutionnel sont écartés en tant que tels dans leur construction.
            Source : https://www.insee.fr/fr/metadonnees/nafr2/sousClasse/01.12Z?champRecherche=false"""),
            html.Div([ dcc.Graph(figure=self.update_1_insee())], style={'width':'100%', }),
            html.Br(),
            html.Br(),

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
            dcc.Markdown("""Somme cumulée du nombre de DPO au cours du temps.
            On peut noter deux tendances : 
                - Pré novembre 2019 : un niveau de croissance rapide et un pic de recrutement en novembre,
                - Post novembre 2019 : un recrutement moins intense.
            On peut donc supposer que la plupart des entreprises se sont soumises aux règles et que les nouveaux recrutements sont plus dues aux créations de nouvelles entités."""),
            
            dcc.Markdown("""Nombre brut de DPO embauchés par mois.
            Remarques générales :
                - Un certain nombre d'entreprises ont commencées à recruter des DPO dès 2018, donc avant le début de l'application de la loi (l'ensemble des DPO enregistrés avant la date d'application sont inscrit durant le premier mois).
                - A partir de 2020 le nombre de DPO enregistrés diminue avec le temps.
            Autres remarques :
                - Certains secteurs d'activité ont été plus enclins à embaucher des DPO dès le départ (secteur financier et et télécommunications, certainement au vue de la criticité de ces services).
                - Il y a un gros pic de recrutement en novembre 2019 dans le secteur de la restauration.
                - Les administrations publiques ont réparties leur recrutement sur 3 ans, ce ne sont pas ces secteurs qui ont été les plus rapides à se mettre au pas."""),
            
            dcc.Markdown("""Somme cumulée du nombre de notifications au cours du temps.
                - La somme des notifications suit globalement une fonction exponentielle, il y a de plus en plus de notifications envoyées par les DPO."""),
            
            dcc.Markdown("""Nombre brut de notifications par mois.
                - L'activité est globalement homogène avec une tendance à la hausse.
                - Le premier mois est vide car les notifications prennent du temps à  être traitées par la CNIL, et seront contées dans le deuxième mois.
                - Il y 2 gros pics de notifications dans 3 secteurs biens précis qui sont : hébergement et restauration, santé humaine et action sociale, activité spécialisées, scientifiques et techniques."""),
            html.Br(),
            
            html.Div([ dcc.Graph(figure=self.update_1_vs()) ], style={'width':'100%', }),
            dcc.Markdown("""Nombre de notifications par rapport au nombre de DPO.
                - Il y a une grande croissance du nombre de notifications par DPO en 2018.
                - La tendance est globalement linéaire et à la hausse.
            Remarque : On pourrait penser que le DPO produisent plus de notifications avec le temps parce qu'ils prennent mieux en charge leur métier. 
            Il s'agit probablement d'une fausse interprétation. En effet dans la mesure où les recrutement des DPO sont déclarés instantanément, contrairement aux notifications qui doivent d'abord être prises en charge par la CNIL, 
            il ne faut pas en déduire que les DPO sont 6 fois plus productifs qu'en début 2018. On peut toutefois noter une légère hausse."""),

            html.Br(),
            html.Br(),

            html.H4(children="Le budget de la CNIL et les montants des sanctions"),
            html.Div([ dcc.Graph(id='rgpd-2-budget-sanctions'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Échelle de l\'axe des ordonnées'),
                           dcc.Dropdown(
                               id='rgpd-2-budget-sanctions-echelle',
                               options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                               value="Linéaire"
                           ),
                         ], style={'width': '18em'})
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
            dcc.Mardown("""Budget de la CNIL et Montant des sanctions.
                - Le budget de la CNIL est quasiment constant sur la période 2012-2021.
                - Avant 2018, le montant des sanctions est bas par rapport à celui de la CNIL.
                - Après la mise en application de la loi de 2018, les sanctions sont plus importantes. On peut justifier cette variation par l'augmentation du nombre global de sanctions ainsi que les sommes de ces sanctions. 
                  En effet certaines amendes sur de grands groupes sont très importantes (Facebook 60 000 000€ en 2020)."""),
            html.Br(),
            html.Br(),

            html.H4(children="Les actions de la CNIL"),
            html.Div([ dcc.Graph(figure=self.update_3_data()) ], style={'width':'100%', }),
            dcc.Markdown("""Evolution du nombre d'actions de la CNIL.
                - Le nombre d'actions qu'effectue la CNIL est assez homogène, voir en baisse en ce qui concerne les contrôles.
                - Ce constat est étonnant en vue du graphique précédent sur les sanctions."""),
            html.Br(),
            
            html.Div([ dcc.Graph(figure=self.update_3_vs()) ], style={'width':'100%', }),
            dcc.Markdown("""Fréquence du nombre d'actions par rapport au nombre de contrôles.
                - On remarque que les avertissements sont peu plébiscités par la CNIL comme les sanctions, bien qu'étant en hausse dernièrement. 
                - De manière générale, la CNIL sanctionne peu par rapport au nombre de contrôles.
                - Le nombre de mise en demeure est assez élevé.
            Mise en demeure : Injonction formelle qui informe une personne que le délai pour remplir une obligation arrive à son terme ou est dépassée. Cette interpellation met en place un nouveau délai qui, s'il n'est pas respecté, oblige la personne à se rendre dans un tribunal.
            Source : https://www.linternaute.fr/dictionnaire/fr/definition/mise-en-demeure/"""),
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

        self.app.callback(
                    dash.dependencies.Output('rgpd-2-budget-sanctions', 'figure'),
                    [ dash.dependencies.Input('rgpd-2-budget-sanctions-echelle', 'value')])(self.update_2_argent)
    
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

        fig.update_layout(
            title = "Nombre de DPO enregistrés / notifications envoyées",
            yaxis = dict( title = cur_ytitle),
            xaxis = dict( title = "Date"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Secteur d\'activité'},
        )
        return fig

    def update_1_vs(self):
        df = (self.notification.sum(axis=1).cumsum() / self.dpo.sum(axis=1).cumsum()).to_frame()
        df.columns = ["Notifications par DPO"]

        fig = px.line(df)

        fig.update_layout(
            title = "Nombre de notifications par rapport au nombre de DPOs",
            yaxis = dict( title = "Nombre de notifications par DPO"),
            xaxis = dict( title = "Date"),
            height=450,
            hovermode='closest',
            showlegend=False
        )
        return fig
    
    def update_2_argent(self, echelle):
        df = self.budget_cnil_sanctions
        df.columns = ["Budget de la CNIL", "Somme des montants des sanctions"]

        fig = px.line(df)

        fig.update_layout(
            title = "Évolution du budget de la CNIL par rapport au montants des sanctions",
            yaxis = dict( title = "Montant en €", type= 'linear' if echelle == 'Linéaire' else 'log',),
            xaxis = dict( title = "Année"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Légende'},
        )
        return fig
    
    def update_3_data(self):
        df = self.sanc_avert_mise_en_demeure_controles

        fig = px.line(df)

        fig.update_layout(
            title = "Évolution du nombre d'actions",
            yaxis = dict( title = "Nombre"),
            xaxis = dict( title = "Année"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Type d\'action'},
        )
        return fig
    
    def update_3_vs(self):
        df = self.sanc_avert_mise_en_demeure_controles.copy()

        df2 = df.iloc[:, :3].div(df["controles"], axis=0)
        df2.columns = [col_name + "/controles" for col_name in df2.columns]

        fig = px.line(df2)

        fig.update_layout(
            title = "Fréquence du nombre d'actions par rapport au nombre de contrôles",
            yaxis = dict( title = "Nombre d'actions par rapport au nombre de contrôles"),
            xaxis = dict( title = "Année"),
            height=450,
            hovermode='closest',
            legend = {'title': 'Rapport'},
        )
        return fig



if __name__ == '__main__':
    rgpd = RGPD()
    rgpd.app.run_server(debug=True, port=8051)
