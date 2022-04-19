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

class Pbmc():
    def __init__(self, application = None):

        self.main_layout = html.Div(children=[
            html.H3(children='PBMC')
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

    def show_hist():    
        color = {    
            "Léger" : "#FFFF00",    
            "mortel" : "#FF0000",    
            "grave non mortel" : "#FF7F00"    
        }    

        figure1 = px.histogram(    
            df,    
            x=df["Année"],    
            color = df["Catégorie véhicule"],    
            facet_col = "Type Accident",    
            facet_col_wrap = 3,    
        )    

    def show_scatter():    
        figure1.update_layout(barmode="stack", bargap=0.2)    
        data = dp.getMortality(df)    

        figure2 = px.scatter_3d(    
             data,    
             x = 'Année',    
             y = 'Age véhicule',    
             z = 'Count',    
             color = 'Type Accident',    
             color_discrete_map=color,    
        )    


        
if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)
