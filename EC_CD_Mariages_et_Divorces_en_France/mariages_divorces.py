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
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import dbf
from simpledbf import Dbf5

class Mariage():
    mar_14 = Dbf5('/data/data mariages 2014.dbf').to_dataframe()
    mar_15 = Dbf5('/data/data mariages 2015.dbf').to_dataframe()
    mar_16 = Dbf5('/data/data mariages 2016.dbf').to_dataframe()
    mar_17 = Dbf5('/data/data mariages 2017.dbf').to_dataframe()
    mar_18 = Dbf5('/data/data mariages 2018.dbf').to_dataframe()
    mar_19 = Dbf5('/data/data mariages 2019.dbf').to_dataframe()
    mar_20 = Dbf5('/data/data mariages 2020.dbf').to_dataframe()

    def filter_df(df):
        df.drop(columns = ['ANAIS1', 'DEPNAIS1', 'INDNAT1', 'ETAMAT1', 'ANAIS2', 'DEPNAIS2', 'INDNAT2','ETAMAT2',
            'JSEMAINE', 'DEPDOM', 'TUDOM', 'TUCOM', 'NBENFCOM'], axis=1, inplace=True)    
    
    filter_df(mar_14)
    filter_df(mar_15)
    filter_df(mar_16)
    filter_df(mar_17)
    filter_df(mar_18)
    filter_df(mar_19)
    filter_df(mar_20)
    
    def __init__(self, application = None):
        df = pd.concat([mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20])

        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph = pd.DataFrame(HH.groupby('AMAR').size(), columns = ['HH'])

        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph = graph.assign(FF = FF.groupby('AMAR').size())

        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph = graph.assign(HF = HF.groupby('AMAR').size())

        graph = graph.assign(TOTAL = df.groupby('AMAR').size().astype(int))

        pd.options.plotting.backend = "plotly"
        graph.plot()
        
        self.df = graph
        self.main_layout = html.Div(children=[
            html.H3(children='Title'),
            html.Div([ dcc.Graph(id='mpj-main-graph'), ], style={'width':'100%', }),
            ])

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                    dash.dependencies.Output('mpj-main-graph', 'figure'),
                    dash.dependencies.Input('mpj-mean', 'value'))(self.update_graph)

    def update_graph(self):
        return self.df

        
if __name__ == '__main__':
    mpj = Deces()
    mpj.app.run_server(debug=True, port=8051)
