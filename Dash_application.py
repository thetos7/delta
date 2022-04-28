import numpy as np
import pandas as pd
import matplotlib
import glob
import plotly.express as px
from os import listdir
#Create dash application
import dash
from dash import Dash, dcc, html, Input, Output, State

class Cancer():
    #Store dataframes:
    def __init__(self, application = None):
        Africa = pd.read_pickle("Africa.pkl", compression="gzip")
        Asia = pd.read_pickle("Asia.pkl", compression="gzip")
        Europe = pd.read_pickle("Europe.pkl", compression="gzip")
        North_america = pd.read_pickle("North_america.pkl", compression="gzip")
        South_america = pd.read_pickle("South_america.pkl", compression="gzip")
        Oceania = pd.read_pickle("Oceania.pkl", compression="gzip")
        World = pd.read_pickle("World.pkl", compression="gzip")
        
        #Insérer la valeur du main layout représentant la page html elle même.
        #self.main_layout = None
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            #self.app.layout = self.main_layout

        app = Dash(__name__)

        self.app.layout = html.Div([
            html.Div(dcc.Input(id='input-on-submit', type='text')),
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id='container-button-basic',
                 children='Enter a value and press submit')
        ])


        self.app.callback(
            Output('container-button-basic', 'children'),
            Input('submit-val', 'n_clicks'),
            State('input-on-submit', 'value')
        )
        
    def update_output(n_clicks, value):
        return 'The input value was "{}" and the button has been clicked {} times'.format(
            value,
            n_clicks
        )


if __name__ == '__main__':
    cncr = Cancer()
    cncr.app.run_server(debug=True)