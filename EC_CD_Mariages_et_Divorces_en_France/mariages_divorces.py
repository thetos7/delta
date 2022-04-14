import sys
import glob
import dash
import flask
from dash import dcc
from dash import html
import json
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
            
        self.L = ['janv', 'fev', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'sept', 'oct','nov','dec']    

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
        
        self.files = [mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20]
        self.dep = '01'
        
        df = pd.concat([mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20])
       
        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph = pd.DataFrame(HH.groupby('AMAR').size(), columns = ['HH'])

        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph = graph.assign(FF = FF.groupby('AMAR').size())

        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph = graph.assign(HF = HF.groupby('AMAR').size())

        graph = graph.assign(TOTAL = df.groupby('AMAR').size().astype(int))
        
        map_f = graph.copy().drop(["HH", "FF", "HF", "TOTAL"], axis=1)
        dep_list = df.groupby("DEPMAR").size().index.tolist()
        
        c = 0
        for idx in dep_list:
            col = df[(df['DEPMAR'] == idx)]
            map_f.insert(c, idx,col.groupby('AMAR').size())
            c += 1
        map_f = map_f.transpose()
        
        mar = mar_14.sort_values(by=['MMAR'])
        mar['Mariage'] = mar['SEXE1'] + mar['SEXE2']
        mar = mar.drop(['AMAR', 'SEXE1', 'SEXE2'], axis=1)
        mar['Mariage'] =  mar['Mariage'].apply(self.str_update)
        mar['MMAR'] =  mar['MMAR'].apply(self.update_month)
        mar = mar.loc[mar['DEPMAR'] == '01']
        mar = mar.drop('DEPMAR', axis=1)

        self.year = 2014
        self.df = graph
        self.map_f = map_f
        self.departements = json.load(open('EC_CD_Mariages_et_Divorces_en_France/data/departements-version-simplifiee.geojson'))
        
        self.fig = px.line(self.df)
        self.fig_map = px.choropleth_mapbox(map_f, geojson=self.departements, locations= map_f.index, featureidkey = 'properties.code', 
                           color=2014, color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={'2014':'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        self.fig_histo = px.bar(mar, x="MMAR", y="Mariage", title="Bla")
               
        self.main_layout = html.Div(children=[
            html.H3(children='Mariages en France'),
            html.Div([
                dcc.Graph(
                    id='mdf-map-graph',
                    figure=self.fig_map,
                    style={'width':'50%', }),
                dcc.Graph(
                    id='mdf-main-graph',
                    figure=self.fig,
                    style={'width':'50%', 'display':'inline-block'}),
                ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            html.Div([
                dcc.Graph(
                    id='mdf-histo-graph',
                    figure=self.fig_histo
                    , style={'width':'100%', }),
                dcc.Slider(id='mdf-crossfilter-year-slider',
                    min=2014,
                    max=2020,
                    step=1,
                    value=2014,
                    marks={str(year): str(year) for year in range(2014, 2021)},)
                ]),
            html.Div(id='slider-output-container')
            ]),

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('mdf-map-graph', 'figure'),
            dash.dependencies.Output('mdf-histo-graph', 'figure'),
            dash.dependencies.Input('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('mdf-map-graph', 'clickData'))(self.update_graph)


    def get_file(self):
           return self.files[self.year - 2014].sort_values(by=['MMAR'])
        
    def update_map(self, year):
        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements,
                        locations= self.map_f.index, featureidkey = 'properties.code', 
                        color=year, color_continuous_scale="Viridis",
                        mapbox_style="carto-positron",
                        zoom=4.6, center = {"lat": 47, "lon": 2},
                        opacity=0.5,
                        labels={year:'Nombre de Mariages'}
                        )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    def update_histo(self):
        mar = self.get_file()
        mar['Mariage'] = mar['SEXE1'] + mar['SEXE2']
        mar = mar.drop(['AMAR', 'SEXE1', 'SEXE2'], axis=1)
        mar['Mariage'] =  mar['Mariage'].apply(self.str_update)
        mar['MMAR'] =  mar['MMAR'].apply(self.update_month)
        mar = mar.loc[mar['DEPMAR'] == self.dep]
        mar = mar.drop('DEPMAR', axis=1)
        
        self.fig_histo = px.bar(mar, x="MMAR", y="Mariage", title="Mariage et divorce dans le %s en %s" % (self.dep, self.year))
        
    def update_graph(self, year, clickData):
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
        if button_id == 'mdf-crossfilter-year-slider':
            self.update_map(year)
            self.year = year
        if button_id == 'mdf-map-graph':
            self.dep = "%02d" % (int(clickData['points'][0]['location']))
        if button_id != 'No clicks yeat':
            self.update_histo()
        
        return self.fig_map, self.fig_histo
    
    def str_update(self, s):
        if s == 'FM':
            return 'MF'
        return s
        
    def update_month(self, s):
        if s not in self.L:
                return self.L[int(s) - 1]
        return s

if __name__ == '__main__':
    mdf = Mariage()
    mdf.app.run_server(debug=True, port=8051)
