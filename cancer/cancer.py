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
        Africa = pd.read_pickle("cancer/data/Africa.pkl", compression="gzip")
        Asia = pd.read_pickle("cancer/data/Asia.pkl", compression="gzip")
        Europe = pd.read_pickle("cancer/data/Europe.pkl", compression="gzip")
        North_america = pd.read_pickle("cancer/data/North_america.pkl", compression="gzip")
        South_america = pd.read_pickle("cancer/data/South_america.pkl", compression="gzip")
        Oceania = pd.read_pickle("cancer/data/Oceania.pkl", compression="gzip")
        World = pd.read_pickle("cancer/data/World.pkl", compression="gzip")
        
        #Insérer la valeur du main layout représentant la page html elle même.
        #self.main_layout = None
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            #self.app.layout = self.main_layout

        app = Dash(__name__)

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de décès par jour en France'),
            html.Div([ dcc.Graph(id='cancer-main-graph'), ], style={'width':'100%', }),
            dcc.RadioItems(
                            id='marginal-option',
                            options=[{'label': i, 'value': i} for i in ['violin', 'rug', 'box']],
                            labelStyle={'display':'block'},
                        )])
        

        self.app.callback(dash.dependencies.Output('cancer-main-graph','figure'),
                          dash.dependencies.Input('currend-df', 'value'),
                          dash.dependencies.Input('column_x', 'value'),
                          dash.dependencies.Input('column_y', 'value'),
                          dash.dependencies.Input('column_color', 'value'),
                          dash.dependencies.Input('marginal_option', 'value'),
                          )(self.update_graph)
        
    def update_graph(self, current_df, column_x, column_y, column_color, marginal_option):
        df = px.data.tips()
        if marginal_option == 'violin' or marginal_option == 'rug' or marginal_option == 'box':
            fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},marginal=marginal_option,text_auto=True)
        else:
            fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},text_auto=True)
        return fig


if __name__ == '__main__':
    cncr = Cancer()
    cncr.app.run_server(debug=True,port=8051)