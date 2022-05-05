import sys
import dash
import flask
from dash import dcc
from dash import html
from dash import callback_context
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class Animal():
    def __init__(self, application = None):
        self.df = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
        self.main_layout = html.Div([
            html.Div([
                html.H3(children='Animal Crossing : New Horizons',
                    style={
                        'font-family' : 'Georgia',
                        'font-weight' : 'bold',
                        'font-size' : '30px',
                        'text-align': 'center'
                        }
                    ),
                html.H4('Les collectables du jeu et leur valeur pécunière',
                    style={
                        'font-family' : 'Georgia',
                        'font-size' : '18px',
                        'text-align' : 'center'
                        }
                    )
                ]),
            html.Button('Poissons', id='bpoisson'),
            html.Button('Insectes', id='binsecte'),
            html.Div([
                dcc.Graph(id='fishY',
                    style={'width' : '75%', 'display':'inline-block'})
                ]),
            html.Div([dcc.Slider(0, 12,
                id='fishy_slider',
                step=None,
                marks={
                    0: "",
                    1: 'Janvier',
                    2: 'Février',
                    3: 'Mars',
                    4: 'Avril',
                    5: 'Mai',
                    6: 'Juin',
                    7: 'Juillet',
                    8: 'Août',
                    9: 'Septembre',
                    10: 'Octobre',
                    11: 'Novembre',
                    12: 'Décembre'
                    },
                value=0,
                )], style={'width' : '75%'})
            ])
        if application:
            self.app = application

        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                dash.dependencies.Output('fishY', 'figure'),
                [dash.dependencies.Input('fishy_slider', 'value')]
                )(changemonth)


        self.app.callback(
            dash.dependencies.Output('fishY', 'figure'),
            [dash.dependencies.Input('bpoisson', 'n_clicks'),
             dash.dependencies.Input('binsecte', 'n_clicks')],
            [dash.dependencies.State('bpoisson', 'id'),
                dash.dependencies.State('binsecte', 'id')]
            )(self.displayGraph)
    
    def displayGraph(self, btn1, btn2, id1, id2):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if id2 + '.n_clicks' == changed_id:
            dfg = pd.read_csv('data/insect.csv')
        else:
            fish = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
            self.df = fish
            fishmonth = fish.filter(regex='SH *', axis = 1)
            fish_count = fishmonth.count()

            res = []

            for i in fish_count:
                res.append(i)

            list_month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
 
            fig = dict({
                "data": [{"type" : "bar",
                            "x" : list_month,
                            "y" : res}],
                "layout": {"title": {"text": "Le nombre de poissons disponible en fonction du mois de l'année"
                    }}
                })
            return fig


    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    ani = Animal()
    ani.run(port=8055)
