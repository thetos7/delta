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
import os

class Ukraine():
    def __init__(self, application = None):
        self.equipement = pd.read_pickle('ukraine/data/russia_losses_equipment.pkl').fillna(0)

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution des prix de différentes énergies en France'),

            html.Div([ dcc.Graph(id='ukr-main-graph'), ], style={'width':'100%', }),

            html.Div([
                html.Div([ html.Div('Champs'),
                           dcc.RadioItems(
                               id='side-type',
                               options=[{'label':'Russie', 'value':0}, 
                                        {'label':'Ukraine','value':1},
                                        {'label':'Russie + Ukraine','value':2}],
                               value=1,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '15em'} ),
                html.Div(style={'width':'2em'}),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. Vous pouvez voir l'equipement en fonction du temps de chaque pays
            
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
                    dash.dependencies.Output('ukr-main-graph', 'figure'),
                    [dash.dependencies.Input('side-type', 'value')])(self.update_graph)
        
    def update_graph(self, side):
        print("in")
        df = self.equipement
        fig = px.line(df[df.columns[0]], template='plotly_white')
        for c in df.columns[2:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
            fig.update_layout(            #title = 'Évolution des prix de différentes énergies',
                yaxis = dict(
                                 type= 'linear'),
                height=450,
                hovermode='closest',
                legend = {'title': 'Énergie'},
                )
        print("out")
        return fig

        
if __name__ == '__main__':
    mpj = Ukraine()
    mpj.app.run_server(debug=True, port=8051)