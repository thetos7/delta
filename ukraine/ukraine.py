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
        self.equipement = pd.read_pickle('ukraine/data/russia_losses_equipment.pkl').fillna(method='ffill')
        self.personnel = pd.read_pickle('ukraine/data/russia_losses_personnel.pkl').fillna(method='ffill')

        self.threads = pd.read_pickle('ukraine/data/threads.pkl').filter(['created_at', 'num_comments', 'score', 'upvote_ratio']).fillna(0)
        self.threads.created_at = self.threads.created_at.apply(lambda x: x[:10])
        self.threads = self.threads.groupby('created_at').agg(list)
        self.threads.num_comments = self.threads.num_comments.apply(lambda x: sum(x))
        self.threads.score = self.threads.score.apply(lambda x: sum(x))
        self.threads.upvote_ratio = self.threads.upvote_ratio.apply(lambda x: sum(x)/float(len(x)))

        self.main_layout = html.Div(children=[
            html.H3(children='Évolution du Stock d\'armement  de la Russie'),
            html.Div([ dcc.Graph(id='equipement-main-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('equipement'),
                           dcc.Dropdown(
                               id='equipement-dropdown',
                               options= [label for label in self.equipement.columns[2:]],
                               value=1,
                               multi=True,
                           )
                         ], style={'width': '15em'} ),
                html.Div([ html.Div('Échelle en y'),
                                dcc.RadioItems(
                                    id='equipement-yaxis-type',
                                    options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                                    value='Logarithmique',
                                    labelStyle={'display':'block'},
                                )
                              ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} )
                              ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. Vous pouvez voir l'equipement en fonction du temps de chaque pays
            
                """),
                html.Br(),
                html.Br(),
                html.Br(),





                html.H3(children='Évolution de l\'armee Russe'),

                 html.Div([ dcc.Graph(id='armee-main-graph'), ], style={'width':'100%', }),

                 html.Div([
                    html.Div([ html.Div('type'),
                                dcc.RadioItems(
                                    id='personnel-type',
                                    options=[{'label':'armee', 'value':0}, 
                                             {'label':'prisonier de guerre','value':1},
                                             {'label':'armee + prisonier de guerre','value':2}],
                                    value=1,
                                    labelStyle={'display':'block'},
                                )
                              ], style={'width': '15em'} ),
                              ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),

                     html.Br(),
                     dcc.Markdown("""
                     Le graphique est interactif. Vous pouvez voir l'equipement en fonction du temps de chaque pays

                     """),

                




                html.Br(),
                html.Br(),
                html.Br(),
                html.H3(children='Evolution des Threads Tweeter'),
                html.Div([ dcc.Graph(id='Tweet-main-graph'), ], style={'width':'100%', }),
                html.Div([
                    html.Div(
                        dcc.Slider(
                                id='tweets-slider',
                                min=0,
                                max=len(self.threads.index),
                                step = 5,
                                value=0,
                                marks={str("day " + str(i)): str("day " + str(i)) for i in range(0,len(self.threads.index),10)},
                        ),
                        style={'display':'inline-block', 'width':"90%"}
                    ),
                    dcc.Interval(            # fire a callback periodically
                        id='wps-auto-stepper',
                        interval=500,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                ),
                html.Div([ dcc.RadioItems(id='tweet-format', 
                                     options=[{'label':'Tweet', 'value':0},
                                              {'label':'Score', 'value':1}, 
                                              {'label':'Ratio', 'value':2}], 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),
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
                    dash.dependencies.Output('equipement-main-graph', 'figure'),
                    [dash.dependencies.Input('equipement-dropdown', 'value'), 
                     dash.dependencies.Input('equipement-yaxis-type', 'value')])(self.update_equipement)
        
        self.app.callback(
                    dash.dependencies.Output('armee-main-graph', 'figure'),
                    [dash.dependencies.Input('personnel-type', 'value')])(self.update_personnel)
        
        self.app.callback(
                    dash.dependencies.Output('Tweet-main-graph', 'figure'),
                    [dash.dependencies.Input('tweet-format', 'value'),
                        dash.dependencies.Input('tweets-slider', 'value'), ])(self.update_tweet)
        
    def update_equipement(self, equipement, axis):
        if not isinstance(equipement, list) or not len(equipement):
            return {}
        else:
            equipement = ["date"] + equipement
        df = self.equipement[equipement]
        df = df.set_index('date')
        fig = px.line(df[df.columns[0]], template='plotly_white')
        
        for c in df.columns[1:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
            fig.update_layout(
                yaxis = dict(type= 'linear' if axis == 'Linéaire' else 'log',),
                height=450,
                hovermode='closest',
                legend = {'title': "equipement"},
                )
        return fig
    
    def update_personnel(self, personnel):
        if personnel == 0:
            select = ["date", "personnel"]
        elif personnel == 1:
            select = ["date", "POW"]
        else:
            select = ["date", "personnel", "POW"]
        df = self.personnel[select]
        df = df.set_index('date')
        fig = px.line(df[df.columns[0]], template='plotly_white')
        
        for c in df.columns[1:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
            fig.update_layout(
                yaxis = dict(type= 'log'),
                height=450,
                hovermode='closest',
                legend = {'title': "equipement"},
                )
        return fig
    
    def update_tweet(self, button, slider):
        tab = ""
        if  button == 0 :
            tab = "num_comments"
        elif button == 1 :
            tab = "score"
        else:
            tab = "upvote_ratio"
        df = self.threads[[tab]].head(slider)
        #fig = px.line(df[df.columns[0]], template='plotly_white')
        #fig.add_scatter(x = df.index, y=df, mode='lines', name=tab, text=tab, hoverinfo='x+y+text')
        #fig.update_layout(
        #        height=450,
        #        hovermode='closest',
        #        )
        fig = px.line(df, template='plotly_white')
        fig.update_layout(
            #title = 'Évolution des prix de différentes énergies',
            xaxis = dict(title=""), # , range=['2010', '2021']), 
            yaxis = dict(title="Nombre de re-tweet par jour"), 
            height=450,
            showlegend=False,
        ) 

        return fig


        
if __name__ == '__main__':
    mpj = Ukraine()
    mpj.app.run_server(debug=True, port=8051)