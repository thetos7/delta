import pandas as pd
import plotly as plt
import os
import glob
import dash
import plotly.express as px
import numpy as np
from dash import dcc
from dash import html
import plotly.graph_objects as go
import PostBacStudies.get_data as gd
from plotly.subplots import make_subplots

class PostBac():


    branches = ['Ecole d\'Ingénieur', 'Ecole de Commerce', 'BTS', 'BUT', 'CPGE', 'Licence', 'EFTS', 'IFSI', 'PACES', 'PASS', 'DUT', 'Management']

    introduction = """
    Bienvenue,
    Dans cette étude nous allons voir l'évolution des voeux et des choix fait par des néo-bacheliers pour leurs études supérieurs entre 2016 et 2021. 
    Cette étude montrera tout d'abord l'impact que parcousup à eu sur les voeux et les choix des étudiants par rapport à APB, puis elle regardera l'évolution globale des voueux et des choix des néo-bacheliers et les inégalités qui peuvent en découler (inégalité homme/femme, inégalier entre étudiant boursier et non-boursier) 
    
    """
    
    admis = """
    On peut voir que le nombre d'admis évolue de manière constant entre 2016 et 2021. Parcousup ayant remplacé APB et 2018, on peut voir que celui-ci n'a pas eu de d'effet conséquent sur le nombre d'admis. On peut tout de même voir qu'il y a un pic d'admis en 2020, explicable par la crise du coronavirus et l'annulation des épreuves du baccalauréat remplacés par les moyennes des notes de Terminale des candidats. Cette méthode a créé un boom du nombre de bacchelier et donc a influé sur le nombre d'admis. 
    """
    def __init__(self, application = None):
        self.df = gd.load_data()
        self.main_layout = html.Div(children=[
            html.H3(children="Evolution des voeux post bac entre 2016 et 2021"),
            html.H5(children='Thomas Chivet et Antoine Vergnaud'),
            html.Div(style={'width' : '100%', 'margin' : 'auto'},
                    children=[dcc.Markdown(PostBac.introduction)],),
            html.H4(children="Nombre d'admis en fonction des annéés"),
            html.Div([ dcc.Graph(id='admis-hist'), ], style={'width':'100%'}),
            html.Div([ dcc.RadioItems(id='hist-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            dcc.Link('Sources', href='https://data.enseignementsup-recherche.gouv.fr/pages/explorer/?q=&sort=modified&refine.keyword=orientation'),
            html.Div(style={'width' : '100%', 'margin' : 'auto'},
                     children=[dcc.Markdown(PostBac.admis)],),
            
            
            html.H4(children="Pourcentage de H/F par fillière"),
            html.Div([ dcc.Graph(id='hf-pie'), ], style = {'width' : '100%', }),
            
            dcc.Link('source', href=''),
            html.Div([ dcc.RadioItems(id='scatter-opts', 
                                     value=2,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.P("Names:"),
            dcc.Dropdown(id='years',
                         options=PostBac.branches,
                         value='BTS', 
                         clearable=False
                        ),
            html.H4(children="Pourcentage de boursier par fillière"),
            html.Div([ dcc.Graph(id='boursier-hist'), ], style={'width':'100%', }),
            dcc.Link('source', href=''),
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
                    dash.dependencies.Output('admis-hist', 'figure'),
                    dash.dependencies.Input('hist-opts', 'value'))(self.show_admis_hist)
        self.app.callback(
                    dash.dependencies.Output('boursier-hist', 'figure'),
                    dash.dependencies.Input('scatter-opts', 'value'))(self.show_boursier_hist)
        self.app.callback(
                    dash.dependencies.Output('hf-pie', 'figure'),
                    dash.dependencies.Input('years', 'value'))(self.show_branch_per_sex)
    
    
    def show_admis_hist(self, mean):  
        fig = px.histogram(
            self.df, 
            x = self.df['Session'],
            y = self.df['Admis'],
            color = 'Filières très agrégées',
            labels={
                 "Session": "Année",
                 "Filières très agrégées": "Filières"
                 },
            )
        fig.update_layout(bargap = 0.2)    
        return fig
        
    def show_boursier_hist(self, mean):  
        df = self.df.groupby(['Session', 'Filières très agrégées'])[['Admis', 'Effectif des admis boursiers']].sum()
        fig = px.histogram(
            df,
            x = df.index.get_level_values(1),
            y = df['Effectif des admis boursiers']*100 / df['Admis'],
            range_y = [0,100],
            color = df.index.get_level_values(1),
            animation_frame=df.index.get_level_values(0),
            labels={
                "sum of y": "Pourcentage",
                 "x": "Fillière",
                 "animation_frame": "Année"
                 },
            )
        fig.update_layout(showlegend=False)
        return fig
        
    def show_branch_per_sex(self, branch):
        years = [2016, 2017, 2018, 2019, 2020, 2021]
        # here we want our grid to be 2 x 3
        rows = 2
        cols = 3
        
        subplot_titles = ["Mixité dans la filière " + branch + ' en ' + str(x) for x in years]

        specs = [[{'type':'domain'}] * cols] * rows
        
        fig = make_subplots(
                rows=rows,
                cols=cols,
                subplot_titles=subplot_titles,
                specs=specs)
        
        fig.update_annotations(font_size=12)
        
        for i, l in enumerate(years):
            
            SexLabels = ["Proportion d'hommes", 'Proportion de femmes']
            my_dict={
            'SEXE': SexLabels,
            'SOMME':[self.df.loc[(self.df['Filières très agrégées'] == branch) & (self.df['Session'] == l)]["Nombre d'hommes"].sum(),
                   self.df.loc[(self.df['Filières très agrégées'] == branch) & (self.df['Session'] == l)]["Nombre de femmes"].sum()]
            }
            dataframe = pd.DataFrame(data = my_dict)
            # basic math to get col and row
            row = i // cols + 1
            col = i % (rows + 1) + 1
            # this is the dataframe for every year
            fig.add_trace(
                go.Pie(labels = dataframe['SEXE'],
                       values = dataframe["SOMME"],
                       showlegend = True,
                       textposition ='inside',
                       textinfo = 'percent'),
                 row = row,
                 col = col

            )

        fig.update_layout(title="", title_x = 0.45)
        return fig

if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)

