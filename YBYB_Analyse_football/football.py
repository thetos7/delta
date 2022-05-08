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

class Football():

    def __init__(self, application = None):

        pd.options.plotting.backend = "plotly"

        leagues = pd.read_csv("YBYB_Analyse_football/data/concat_leagues/leagues.csv")

        league_colors = {'liga':'gold', 'PL':'blue', 'serieA':'green', 'ligue1':'black', 'bundesliga':'red'}

        fig = px.scatter(leagues, x='Rk', y='Age', color="league", hover_name="Squad", 
                color_discrete_map=league_colors, title="Déplacez la souris sur une bulle pour avoir les graphiques du club en bas.",
                size = 'Market Value', 
                size_max=60, 
                animation_frame=leagues["Years"], animation_group="Squad", range_y=[leagues['Age'].min(), leagues['Age'].max()], range_x=[1,20])
                
        self.main_layout = html.Div(children=[
            html.H3(children='Classement en fonction de l age et de la valeur marchande des clubs'),
            html.Div([ dcc.Graph(figure=fig), ], style={'width':'100%', }),
            html.Br(), 
            dcc.Markdown("""
            Notes: 
            - On peut donc constater que plus la valeur marchande de l'équipe est élevée plus son classement est meilleur. 
            - On constate aussi que l'equipe à un meilleur classement si la moyenne d'age de l'équipe est entre 22 ans et 26 ans. 
             En effet une équipe trop jeune manque d'expérience et une équipe agée manque d'intensité dans le jeu. 
            - Nous remarquons qu'il peut y avoir des exceptions tel que le club Leicester City (en PL) qui est classé premier, dans la saison 2015-16, alors que sa valeur marchande est faible par raport à d'autres club.
            Nous notons aussi que le Bayern Munich (en Bundeshliga) est classé premier dans la saison 2005-06 alors que l'age moyen des joueurs est de 27,692308 ans. 
            
            ### A propos
            Nous nommons les top5 ligues les ligues suivantes: 
            - Liga -> ligue espagnol
            - PL -> ligue anglaise 
            - Ligue 1 -> ligue française
            - Bundeshliga -> ligue allemande
            * Sources : 
                * [Valeur Marchande de chaque club dans les top 5 ligues](https://www.transfermarkt.com/spieler-statistik/wertvollstemannschaften/marktwertetop)
                * [Classement des top 5 ligues](https://fbref.com/en/comps/9/26/1992-1993-Premier-League-Stats)
                * [Age de tous les joueurs de chaque clubs dans les top5 ligues](https://github.com/ewenme/transfers)
            * (c) 2022 Youssef BOUARFA DINIA et Yassin BOUHASSOUN
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
        
if __name__ == '__main__':
    foot = Football()
    foot.app.run_server(debug=True, port=8051)
