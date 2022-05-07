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
            
        def convert(i):
            return int(i)

            
        self.L = ['janv', 'fev', 'mars', 'avril', 'mai', 'juin', 'juillet', 'aout', 'sept', 'oct','nov','dec']    

        mar_14 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2014.csv", sep=',', low_memory=False)
        mar_15 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2015.csv", sep=',', low_memory=False)
        mar_16 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2016.csv", sep=',', low_memory=False)
        mar_17 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2017.csv", sep=',', low_memory=False)
        mar_18 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2018.csv", sep=',', low_memory=False)
        mar_19 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2019.csv", sep=',', low_memory=False)
        mar_20 = pd.read_csv("EC_CD_Mariages_et_Divorces_en_France/data/data_mariages_2020.csv", sep=',', low_memory=False)
        mar = pd.read_excel('EC_CD_Mariages_et_Divorces_en_France/data/mariages par mois.xls', skiprows = {0,1, 2, 3, 5, 6},
                            usecols = { 'Ensemble des mariages de l\'année', 'Mois du mariage',
                                       'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre',
                                       'Octobre', 'Novembre', 'Décembre'}, skipfooter = 1, dtype=int)
        pacs = pd.read_excel('EC_CD_Mariages_et_Divorces_en_France/data/ensemble des pacs.xlsx',
                             skiprows = {0,1, 2, 4}, usecols = {0, 4,5,6}, skipfooter = 16)
        
        filter_df(mar_14)
        filter_df(mar_15)
        filter_df(mar_16)
        filter_df(mar_17)
        filter_df(mar_18)
        filter_df(mar_19)
        filter_df(mar_20)
        
        self.files = [mar_14, mar_15, mar_16, mar_17, mar_18, mar_19, mar_20]
        self.dep = '01'
        
        deps = pd.read_excel('EC_CD_Mariages_et_Divorces_en_France/data/departements-francais.xls',
                             usecols = {'NOM', 'NUMÉRO'}, skipfooter = 7)
        deps.rename(columns={'NUMÉRO' : 'DEPARTEMENT'}, inplace = True)
            
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
        map_f.reset_index(drop = True, inplace = True)
        map_f = pd.concat([map_f, deps], axis=1)
        for i in range (0,10):
            map_f.loc[map_f.DEPARTEMENT == i, "DEPARTEMENT"] = "0%i" % i
            
        graph = graph.reset_index()
        graph['AMAR'] =  graph['AMAR'].apply(convert)    
            
            
            
        
        
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
       
        self.year = 1946
        self.df = graph
        self.map_f = map_f
        self.departements = json.load(open('EC_CD_Mariages_et_Divorces_en_France/data/departements-version-simplifiee.geojson'))
        
        self.fig = px.line(graph)

        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations=self.map_f.DEPARTEMENT,
                           hover_name = self.map_f.NOM,
                           featureidkey = 'properties.code', 
                           color=2014, range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        self.fig_histo = px.histogram(graph2, x = 'MMAR', y = ['HH', 'FF', 'HF'], barmode='group')
        self.fig.update_layout(
            title = 'Mariages en France depuis 2014',
            xaxis = dict(title = 'Année de l\'Union'),
            yaxis = dict(title = 'Nombre d\'Union'), 
            legend = dict(title = 'Type d\'Union')
        )
        self.fig_histo.update_layout(
            title = 'Mariage et divorce %s en %s' % (self.dep_name(), self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage') 
        )
               
        self.main_layout = html.Div(children=[
            html.H3(children='Mariages en France'),
            html.Div([
                dcc.Graph(
                    id='mdf-map-graph',
                    #figure=self.fig_map,
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
                    dcc.Slider(id='mdf-crossfilter-year-slider',
                        min=1946,
                        max=2020,
                        step=1,
                        value=1946,
                        marks={str(year): str(year) for year in range(1945, 2021, 5)},),
                    dcc.Interval(
                        id='mdf-auto-stepper',
                        interval=1000,
                        max_intervals = -1,
                        n_intervals = 0
                        ),
                        ], style={
                            'padding': '0px 50px', 
                            'width':'90%'
                        }),
            html.Button(
                self.START,
                id='mdf-button-start-stop', 
                style={'display':'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='mdf-histo-graph',
                    figure=self.fig_histo
                    , style={'width':'100%', })
                    ]),
                        html.Br(),
            dcc.Markdown(
                """
                La carte est interactive. En cliquant sur un département, l'histogramme affichera les données sur le département sélectionné. 
                Notes :
               * 17 mai 2013
               * HH : Mariage Homme-Homme
               * FF : Mariage Femme-Femme
               * HF : Mariage Homme-Femme
            #### À propos
            * Sources : https://www.insee.fr/fr/statistiques
            * (c) 2022 Elodine Coquelet & Calliopee Desenfans
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
        opa = 0 if self.year < 2014 else 0.5
        year = self.year if self.year > 2013 else 2014
        self.fig_map = px.choropleth_mapbox(self.map_f, geojson=self.departements, locations= self.map_f.DEPARTEMENT,
                           hover_name = self.map_f.NOM,
                           featureidkey = 'properties.code', 
                           color=year, range_color=[200, 10000], color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=opa,
                           labels={self.year:'Nombre de Mariages'}
                          )
        self.fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    
    #TODO : mettre le nom département en titre Saloperie de Corse option de secours faire une fonction qui retourne ce qu'il faut
    def update_histo(self):
        if self.year < 2014:
            return
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
        
        self.fig_histo = px.histogram(graph, x = 'MMAR', y = ['HH', 'FF', 'HF'], barmode='group')
        
        self.dep_name
        self.fig_histo.update_layout(
            title = 'Mariage et divorce %s en %s' % (self.dep_name(), self.year),
            xaxis = dict(title = 'Mois du mariage'),
            yaxis = dict(title = 'Nombre de mariages'), 
            legend = dict(title = 'Type de mariage') 
        )
        
    def update_graph(self, year, clickData):
        ctx = dash.callback_context
        button_id =""
        if ctx.triggered:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
        if button_id == 'mdf-crossfilter-year-slider':
            self.year = year
            self.update_map()
        if button_id == 'mdf-map-graph':
            self.dep = str(clickData['points'][0]['location'])
        self.update_histo()
        
        return self.fig_map, self.fig_histo
    
    def str_update(self, s):
        if s == 'FM':
            return 'MF'
        return s
        
    def update_month(self, s):
        return self.L[int(s) - 1]
    
    def check_months(self, graph):
        col = graph['MMAR'].unique()
        idx = len(col)
    
        for i in range(1, 13):
            if i < 10:
                s = "0" + str(i)
            else:
                s = str(i)
            if i not in col :
                graph.loc[idx] = (int(s), 0,0, 0.0001)
                idx += 1
        return graph
    
    def dep_name(self):
        if self.dep == "2A" or self.dep == "2B" or int(self.dep) < 10:
            return self.map_f[self.map_f['DEPARTEMENT'] == self.dep].iloc[0,7]
        else:
            return self.map_f[self.map_f['DEPARTEMENT'] == int(self.dep)].iloc[0,7]
    
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
        if text == self.STOP:
            if self.year < 2014:
                self.year += 1
                return self.year
            if self.dep == '19':
                self.dep = '2A'
            elif self.dep == '2A':
                self.dep = '2B'
            elif self.dep == '2B':
                self.dep = '21'
            elif self.dep == '95':
                self.dep = '01'
                if year == 2020:
                    self.year = 1946
                else:
                    self.year += 1
            else:
                tmp = int(self.dep) + 1
                self.dep = str(tmp) if tmp > 9 else "0" + str(tmp)
                
        return self.year 

if __name__ == '__main__':
    mdf = Mariage()
    mdf.app.run_server(debug=True, port=8051)
