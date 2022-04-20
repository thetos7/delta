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
import pbmc_accidents_routiers_type_age_vehicule.data.get_data as dp

class Pbmc():
    def __init__(self, application = None):
        self.df = dp.loadData()
        self.main_layout = html.Div(children=[
            html.H3(children="Mortalité des accidents routiers en France, en fonction du type et l'age du véhicule"),
            html.H5(children='Philippe Bouchet et Michail Chatzizacharias'),
            html.H4(children="Gravité des accidents en relation avec les catégories des véhicules"),
            html.Div([ dcc.Graph(id='pbmc-hist'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='hist-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            dcc.Link('source', href='https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/'),
            html.H4(children="Gravité des accidents en relation avec l'age des véhicules"),
            html.Div([ dcc.Graph(id='pbmc-scatter'), ], style={'width':'100%', }),
            dcc.Link('source', href='https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2020/'),
            html.Div([ dcc.RadioItems(id='scatter-opts', 
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
                    dash.dependencies.Output('pbmc-hist', 'figure'),
                    dash.dependencies.Input('hist-opts', 'value'))(self.show_hist)
        self.app.callback(
                    dash.dependencies.Output('pbmc-scatter', 'figure'),
                    dash.dependencies.Input('scatter-opts', 'value'))(self.show_scatter)

    def show_hist(self, mean):    
        fig = px.histogram(    
            self.df,    
            x=self.df["Année"],    
            color =self.df["Catégorie véhicule"],    
            facet_col = "Type Accident",    
            facet_col_wrap = 3,    
        )
        fig.update_layout(barmode="stack", bargap=0.2)    
        return fig

    def show_scatter(self, mean):    
        color = {    
            "Léger" : "#FFFF00",    
            "mortel" : "#FF0000",    
            "grave non mortel" : "#FF7F00"    
        }    
        data = dp.getMortality(self.df)    

        fig2 = px.scatter_3d(    
             data,    
             x = 'Année',    
             y = 'Age véhicule',    
             z = 'Count',    
             color = 'Type Accident',    
             color_discrete_map=color,    
        )    

        return fig2
 
if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)
