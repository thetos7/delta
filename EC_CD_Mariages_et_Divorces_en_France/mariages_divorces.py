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
    START = 'Start'
    STOP  = 'Stop'
    
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
        
        df = mar_14
        df = df[df['DEPMAR'] == self.dep] 
      
        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph2 = pd.DataFrame(HH.groupby('MMAR').size(), columns = ['HH'])
        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph2 = graph2.assign(FF = FF.groupby('MMAR').size())
        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph2 = graph2.assign(HF = HF.groupby('MMAR').size())
        
        graph2 = graph2.reset_index()
        graph2 = self.check_months(graph2)
        graph2 = graph2.sort_values(by=['MMAR'])
        graph2['MMAR'] =  graph2['MMAR'].apply(self.update_month)
       
        self.year = 2014
        self.df = graph
        self.map_f = map_f
        self.departements = json.load(open('EC_CD_Mariages_et_Divorces_en_France/data/departements-version-simplifiee.geojson'))
        
        self.fig = px.line(self.df)
        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations= self.map_f.index,
                           featureidkey = 'properties.code', 
                           color=self.year, range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        self.fig_histo = px.histogram(graph2, x = 'MMAR', y = ['HH', 'FF', 'HF'], barmode='group',)
        self.fig.update_layout(
            title = 'Mariages en France depuis 2014',
            xaxis = dict(title = 'Année du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage')
    
        )
        self.fig_histo.update_layout(
            title = 'Mariage et divorce dans le %s en %s' % (self.dep, self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage') 
        )
               
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
                    marks={str(year): str(year) for year in range(2014, 2021)},),
                dcc.Interval(
                    id='mdf-auto-stepper',
                    interval=1000,
                    max_intervals = -1,
                    n_intervals = 0
                    ),
                    ], style={
                        'padding': '0px 50px', 
                        'width':'100%'
                    }),
            html.Button(
                self.START,
                id='mdf-button-start-stop', 
                style={'display':'inline-block'}),
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
        self.app.callback(
            dash.dependencies.Output('mdf-button-start-stop', 'children'),
            dash.dependencies.Input('mdf-button-start-stop', 'n_clicks'),
            dash.dependencies.State('mdf-button-start-stop', 'children'))(self.change_button)
        self.app.callback(
            dash.dependencies.Output('mdf-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('mdf-button-start-stop', 'children')])(self.run_movie)
        self.app.callback(
            dash.dependencies.Output('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('mdf-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('mdf-crossfilter-year-slider', 'value'),
            dash.dependencies.State('mdf-button-start-stop', 'children')])(self.on_interval)


    def get_file(self):
           return self.files[self.year - 2014].sort_values(by=['MMAR'])
        
    def update_map(self):
        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations= self.map_f.index,
                           featureidkey = 'properties.code', 
                           color=self.year, range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    def update_histo(self):
        print('in histo')
        df = self.get_file()
        df = df[df['DEPMAR'] == self.dep] 
      
        HH = df[(df['SEXE1'] == 'M') & (df['SEXE2'] == 'M')]
        graph = pd.DataFrame(HH.groupby('MMAR').size(), columns = ['HH'])
        FF = df[(df['SEXE1'] == 'F') & (df['SEXE2'] == 'F')]
        graph = graph.assign(FF = FF.groupby('MMAR').size())
        HF = df[((df['SEXE1'] == 'M') & (df['SEXE2'] == 'F')) | ((df['SEXE1'] == 'F') & (df['SEXE2'] == 'M'))]
        graph = graph.assign(HF = HF.groupby('MMAR').size())
        
        graph = graph.reset_index()
        graph = self.check_months(graph)
        graph = graph.sort_values(by=['MMAR'])
        graph['MMAR'] =  graph['MMAR'].apply(self.update_month)
        
        self.fig_histo = px.histogram(graph, x = 'MMAR', y = ['HH', 'FF', 'HF'],
                                      title="Mariage et divorce dans le %s en %s" % (self.dep, self.year), barmode='group')
        self.fig_histo.update_layout(
            title = 'Mariage et divorce dans le %s en %s' % (self.dep, self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage') 
        )
        
    #Note : self.update_histo probablement reset legende
    def update_graph(self, year, clickData):
        print("on graph")
        ctx = dash.callback_context
        button_id =""
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
        if button_id == 'mdf-crossfilter-year-slider':
            self.year = year
            self.update_map()
        if button_id == 'mdf-map-graph':
            self.dep = clickData['points'][0]['location']
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
    
    def check_months(self, graph):
        col = graph['MMAR'].unique()
        idx = len(col)
    
        for i in range(1, 13):
            if i < 10:
                s = "0" + str(i)
            else:
                s = str(i)
            if s not in col :
                graph.loc[idx] = (int(s), 0,0, 0.0001)
                idx += 1
        return graph
    
    def change_button(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START
    
    def run_movie(self, text):
        if text == self.START:
            return 0 
        else:
            return -1
        
    def on_interval(self, n_intervals, year, text):
        print("in")
        if text == self.STOP:
            if self.dep == '19':
                self.dep = '2A'
            elif self.dep == '2A':
                self.dep = '2B'
            elif self.dep == '2B':
                self.dep = '21'
            elif self.dep == '95':
                self.dep = '01'
                if year == 2020:
                    self.year = 2014
                else:
                    self.year += 1
            else:
                tmp = int(self.dep) + 1
                self.dep = str(tmp) if tmp > 9 else "0" + str(tmp)
                
        return self.year 

if __name__ == '__main__':
    mdf = Mariage()
    mdf.app.run_server(debug=True, port=8051)
