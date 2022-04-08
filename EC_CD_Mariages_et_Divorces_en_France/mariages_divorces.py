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

class Mariage():
    
    def __init__(self, application = None):
        def filter_df(df):
            df.drop(columns = ['ANAIS1', 'DEPNAIS1', 'INDNAT1', 'ETAMAT1', 'ANAIS2', 'DEPNAIS2', 'INDNAT2','ETAMAT2',
                    'JSEMAINE', 'DEPDOM', 'TUDOM', 'TUCOM', 'NBENFCOM'], axis=1, inplace=True)

        mar_14 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2014.csv", sep=',', low_memory=False)
        mar_15 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2015.csv", sep=',', low_memory=False)
        mar_16 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2016.csv", sep=',', low_memory=False)
        mar_17 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2017.csv", sep=',', low_memory=False)
        mar_18 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2018.csv", sep=',', low_memory=False)
        mar_19 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2019.csv", sep=',', low_memory=False)
        mar_20 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2020.csv", sep=',', low_memory=False)
        filter_df(mar_14)
        filter_df(mar_15)
        filter_df(mar_16)
        filter_df(mar_17)
        filter_df(mar_18)
        filter_df(mar_19)
        filter_df(mar_20)
        
        df = pd.concat([mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20])
       
        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph = pd.DataFrame(HH.groupby('AMAR').size(), columns = ['HH'])

        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph = graph.assign(FF = FF.groupby('AMAR').size())

        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph = graph.assign(HF = HF.groupby('AMAR').size())

        graph = graph.assign(TOTAL = df.groupby('AMAR').size().astype(int))

        self.df = graph

        fig = px.line(self.df)

        self.main_layout = html.Div(children=[
            html.H3(children='Title'),
            html.Div([
                dcc.Graph(
                    id='mdf-main-graph',
                    figure=fig
                    )
                ]),
            html.Div([
                dcc.Slider(
                    id='mdf-crossfilter-year-slider',
                    min=2014,
                    max=2020,
                    step=1,
                    value=2014,
                    marks={str(year): str(year) for year in range(2014, 2021)},)
                    ]),
            ]),

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        @self.app.callback(
            dash.dependencies.Output("mdf-main-graph", "figure"),
                [dash.dependencies.Input("mdf-main-type", "value")])
        def update_line_chart(self, tmp):
            fig = px.line(self.df)
            return fig


if __name__ == '__main__':
    mdf = Mariage()
    mdf.app.run_server(debug=True, port=8051)
