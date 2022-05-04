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
import tdmr_quality_of_life_and_worktime.data.get_data as data

class Tdmr():
    def __init__(self, application = None):
        self.complete_dataframe, self.hapiness_dataframe = data.get_complete_dataframes()
        self.main_layout = html.Div(children=[
            html.H3(children="Impact du temps de travail sur la vie en Europe"),
            html.H5(children="Tanguy Desgouttes et Marc-Emmanuel Raiffe"),
            html.P("L'idée derrière ce sujet inspirée entre autre par un subreddit (r/antiwork) est de voir si il se dégage une relation ou tendance générale entre le temps de travail moyen des habitants d'un pays et la qualité de leur vie."),
            html.P("Pour cela on compare ici la moyenne du temps de travail par pays en Europe différents facteurs."),
            
            html.Br(),
            html.H4(children="Note moyenne de satisfaction dans la vie et temps de travail hebdomadaire moyen par pays"),
            html.Div([ dcc.Graph(id='satisfaction_graph'), ], style={'width':'100%', }),
            
            html.H4(children="Proportion de symptomes dépressifs et temps de travail hebdomadaire moyen par pays"),
            html.Div([ dcc.Graph(id='depression_graph'), ], style={'width':'100%', }),
            html.P("Grace aux deux graphiques précédents et à la régression linéaire affichée on voit une légère tendance se dessiner."),
            html.P("Les longs temps de travail semblent impacter négativement la note moyenne que les gens attribuent à leur satisfaction."),
            html.P("D'un autre côté ces mêmes longs temps de travail semblent impacter positivement le taux de symptomes dépressifs en les réduisant."),
            html.P("Naivement on pourrait penser grace à ces données européennes que les gens perçoivent les longs temps de travail comme un poids sur leur satisfaction mais également qu'ils pourraient être un frein au temps libre et à l'introspection, rendant moins courante l'appartion de symptomes dépressifs."),
            html.Br(),
            
            html.H4(children="Espérance de vie et temps de travail hebdomadaire moyen par pays"),
            html.Div([ dcc.Graph(id='expectancy_graph'), ], style={'width':'100%', }),
            html.P("Il semble se dessiner ici que l'espérance de vie moyenne est négativement impactée par les longs temps de travail hebdomadaire."),
            html.Br(),
            
            html.H4(children="Fréquence de sentiment de bonheur et temps de travail hebdomadaire moyen par pays"),
            html.Div([ dcc.Graph(id='hapiness_graph'), ], style={'width':'100%', }),
            html.P("Ce dernier graphe vient renforcer l'idée offerte par le premier en y apportant des détails. Analysons le en deux points :"),
            html.Ul(children=[
                html.Li("On voit que dans les pays avec un temps de travail moyen inférieur les gens donnent plus souvent des réponses positives comme toujours ou la plupart du temps, visible à leur deux pents descendentes"),
                html.Li("A l'inverse les autres réponses plus négatives sont toutes en moyenne plus présentes dans les pays où le temps de travail moyen est plus élevé"),
            ]),
            html.P(""),
            html.Br(),
            
            
            html.H4(children="Sources des données : "),
            dcc.Link("Chiffres sur le nombre moyen d'heures de travail habituellement prestées par semaine dans les pays d'Europe", href='https://ec.europa.eu/eurostat/databrowser/view/LFSA_EWHUN2__custom_2616289/default/table?lang=fr'),
            html.Br(),
            dcc.Link("Chiffres sur la note de satifaction dans sa vie personnelle dans les pays d'Europe", href='https://ec.europa.eu/eurostat/databrowser/view/ILC_PW01__custom_2616313/default/table?lang=fr'),
            html.Br(),
            dcc.Link("Chiffres sur la proporation de symptomes dépressifs dans les pays d'Europe", href='https://ec.europa.eu/eurostat/databrowser/view/HLTH_EHIS_MH1E__custom_2627991/default/table?lang=fr'),
            html.Br(),
            dcc.Link("Chiffres sur l'espérance de vie dans les pays d'Europe", href='https://ec.europa.eu/eurostat/databrowser/view/demo_mlexpec$DV_292/default/table?lang=fr'),
            html.Br(),
            dcc.Link("Chiffres sur la fréquence de sentiment de bonheur pendant un mois dans les pays d'Europe", href='https://ec.europa.eu/eurostat/databrowser/view/ilc_pw08$DV_426/default/table?lang=fr'),
            
            
            html.Div([ dcc.RadioItems(id='satisfaction_block', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Div([ dcc.RadioItems(id='depression_block', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Div([ dcc.RadioItems(id='expectancy_block', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Div([ dcc.RadioItems(id='hapiness_block', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('satisfaction_graph', 'figure'),
                    dash.dependencies.Input('satisfaction_block', 'value'))(self.show_satisfaction)
        self.app.callback(
                    dash.dependencies.Output('depression_graph', 'figure'),
                    dash.dependencies.Input('depression_block', 'value'))(self.show_depression)
        self.app.callback(
                    dash.dependencies.Output('expectancy_graph', 'figure'),
                    dash.dependencies.Input('expectancy_block', 'value'))(self.show_expectancy)
        self.app.callback(
                    dash.dependencies.Output('hapiness_graph', 'figure'),
                    dash.dependencies.Input('hapiness_block', 'value'))(self.show_hapiness)

    def show_satisfaction(self, mean):    
        fig = px.scatter(    
            self.complete_dataframe,    
            x=self.complete_dataframe["Temps de travail par semaine"],    
            y=self.complete_dataframe["Note de satisfaction dans la vie (/10)"],
            color =self.complete_dataframe["Pays"],    
            trendline="ols",
            trendline_scope="overall"
        )
        return fig

    def show_depression(self, mean):    
        fig = px.scatter(    
            self.complete_dataframe,    
            x=self.complete_dataframe["Temps de travail par semaine"],    
            y=self.complete_dataframe["Part de symptomes dépressifs (%)"],
            color=self.complete_dataframe["Pays"],
            trendline="lowess",
            trendline_scope="overall"
        )
        return fig
    
    def show_expectancy(self, mean):    
        fig = px.scatter(    
            self.complete_dataframe,    
            x=self.complete_dataframe["Temps de travail par semaine"],    
            y=self.complete_dataframe["Espérance de vie"],
            color=self.complete_dataframe["Pays"],
            trendline="ols",
            trendline_scope="overall"
        )
        return fig
    
    def show_hapiness(self, mean):    
        fig = px.scatter(    
            self.hapiness_dataframe,    
            x=self.hapiness_dataframe["Temps de travail par semaine"],    
            y=self.hapiness_dataframe["Fréquence du sentiment de bonheur au cours du dernier mois"],
            color=self.hapiness_dataframe["Fréquence"],
            trendline="ols",
            category_orders={"Fréquence": ["Toujours", "La plupart du temps", "Parfois", "Rarement", "Jamais"]}
        )
        return fig

if __name__ == '__main__':
    mpj = Tdmr()
    mpj.app.run_server(debug=True, port=8051)