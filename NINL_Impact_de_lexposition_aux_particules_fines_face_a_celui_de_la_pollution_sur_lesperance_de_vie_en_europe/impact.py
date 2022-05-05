import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du
from urllib.request import urlopen
import json

data_path = "NINL_Impact_de_lexposition_aux_particules_fines_face_a_celui_de_la_pollution_sur_lesperance_de_vie_en_europe/data/"
class Impact():
    def __init__(self, application = None):
        self.countries_fr_to_en = {
            'Albanie': 'Albania',
            'Allemagne': 'Germany',
            'Arménie': 'Armenia',
            'Autriche': 'Austria',
            'Belgique': 'Belgium',
            'Bosnie-Herzégovine':'Bosnia and Herzegovina',
            'Bulgarie': 'Bulgaria',
            'Chypre': 'Cyprus',
            'Croatie': 'Croatia',
            'Danemark': 'Denmark',
            'Espagne': 'Spain',
            'Estonie': 'Estonia',
            'Finlande': 'Finland',
            'France': 'France',
            'Grèce': 'Greece',
            'Hongrie': 'Hungary',
            'Irlande': 'Ireland',
            'Islande': 'Iceland',
            'Italie': 'Italy',
            'Lettonie': 'Latvia',
            'Lituanie': 'Lithuania',
            'Luxembourg': 'Luxembourg',
            'Malte': 'Malta',
            'Moldavie': 'Moldova',
            'Macédoine': 'North Macedonia',
            'Montenegro': 'Montenegro',
            'Norvège': 'Norway',
            'Pays-Bas': 'Netherlands',
            'Pologne': 'Poland',
            'Roumanie': 'Romania',
            'Royaume-Uni': 'United Kingdom',
            'Serbie': 'Serbia',
            'Slovaquie': 'Slovakia',
            'Slovénie': 'Slovenia',
            'Suède': 'Sweden',
            'Suisse': 'Switzerland',
            'Tchéquie': 'Czechia',
            'Turquie': 'Turkey',
            'Ukraine': 'Ukraine',
        }

        self.fine_particles = pd.read_pickle(data_path + "fine_particles_2008-2019.pkl")
        self.lifespan = pd.read_pickle(data_path + "lifespan_2008-2019.pkl")
        self.pollution = pd.read_pickle(data_path + "pollution_2008-2019.pkl")

        self.countries = np.intersect1d(self.fine_particles['country'], self.lifespan['country'])
        self.countries = np.intersect1d(self.countries, self.pollution['country'])

        self.main_layout = html.Div(children=[
            html.H3(children='Impact de l\'exposition aux particules fines face à celui de la pollution sur l\'espérance de vie en Europe'),
            html.Div([ 
                html.Div([
                    dcc.Graph(id='imp-pollution-graph', figure=self.set_graph(self.pollution, "pollution"), style={'width':'100%', 'display':'inline-block'}),
                    dcc.RadioItems(
                        id='imp-pollution-type',
                        options=[{'label':'Graphe', 'value':0},
                                {'label':'Carte', 'value':1}],
                        value=0,
                        labelStyle={'display':'block'},
                    )], style={'width':'50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='imp-particles-graph', figure=self.set_graph(self.fine_particles, "particules fines"), style={'width':'100%', 'display':'inline-block'}),
                    dcc.RadioItems(
                        id='imp-particles-type',
                        options=[{'label':'Graphe', 'value':0},
                                {'label':'Carte', 'value':1}],
                        value=0,
                        labelStyle={'display':'block'},
                    )], style={'width':'50%', 'display': 'inline-block'}),                   
                ], style={'width':'100%', }),
            html.Br(),
            html.Br(),
            dcc.Markdown("""
            #TODO préciser différence pollution particules fines
            Il est possible d'intervertir le graphe avec une carte qui montre le ratio entre l'espérance de vie et le taux de pollution d'un côté, et le ratio entre l'espérance de vie et le taux de particules fines de l'autre.

            Même si les résultats semblent similaires tant dans les graphes que sur les cartes, nous pouvons ressortir quelques pistes de lecture :
            * Sur le graphe, plus la courbe d'un pays se trouve sur des abscisses élevées, plus son exposition à la pollution ou au taux de particules fines est importante.
            * L'échelle des cartes est plus grande pour le ratio du taux de pollution. Cela signifie que que le taux de particules fines est globalement plus élevée que le taux de pollution en Europe. 
            """),
            html.Br(),
            html.Br(),
            dcc.Graph(id='imp-ratio-graph', figure=self.set_ratio_graph(), style={'width':'100%', 'display':'inline-block'}),
            dcc.Markdown("""
            Ce graphe montre le ratio entre les 2 ratios calculés pour les cartes.
            # TODO
            """)
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
            dash.dependencies.Output('imp-pollution-graph', 'figure'),
            [dash.dependencies.Input('imp-pollution-type', 'value'),])(self.set_pollution_figure)

        self.app.callback(
            dash.dependencies.Output('imp-particles-graph', 'figure'),
            [dash.dependencies.Input('imp-particles-type', 'value'),])(self.set_particles_figure)


    def set_pollution_figure(self, dataframe_type):
        if dataframe_type == 1:
            return self.set_map(self.pollution, "pollution") 
        else:
            return self.set_graph(self.pollution, "pollution")

    def set_particles_figure(self, dataframe_type):
        if dataframe_type == 1:
            return self.set_map(self.fine_particles, "particules fines") 
        else:
            return self.set_graph(self.fine_particles, "particules fines")

    def set_graph(self, dataframe, name):
        fig = px.line(template='plotly_white')
        for country in self.countries:
            dataframe_values = dataframe.loc[dataframe['country'] == country]
            lifespan_values = self.lifespan.loc[self.lifespan['country'] == country]
            values = pd.merge(lifespan_values, dataframe_values, left_on=['year', 'country'], right_on=['year', 'country'], suffixes = ['_lifespan', ''])
            values.value = values.value.astype(float)
            values = values.sort_values(by=['value'])
            fig.add_scatter(x = values.value, y=values.value_lifespan, mode='lines', name=country, text=country, hoverinfo='x+y+text')
        xtitle = "Taux de " + name
        ytitle = "Espérance de vie"
        fig.update_layout(
            title = 'Evolution de l\'espérance de vie en fonction du taux de ' + name + ' en Europe',
            xaxis = dict( title = xtitle,
                          type= 'linear',),
            yaxis = dict( title = ytitle,
                          type= 'linear',),
            height=450,
            hovermode='closest',
            legend = {'title': 'Pays'},
        )
        return fig

    def set_map(self, dataframe, name):
        values = []
        text = []
        for country in self.countries_fr_to_en:
            if country in self.countries:
                dataframe_values = dataframe.loc[dataframe['country'] == country].reset_index(drop=True)
                lifespan_values = self.lifespan.loc[self.lifespan['country'] == country].reset_index(drop=True)
                ratios = lifespan_values.value.astype(float) / dataframe_values.value.astype(float)
                ratio_mean = ratios.mean()
                values.append(float("{:.3f}".format(ratio_mean)))
                text.append("")
            else:
                values.append(0)
                text.append("No data")

        with open(data_path + "europe.geo.json") as json_data:
            europe = json.load(json_data)
        
        fig = go.Figure([
            go.Choropleth(
            geojson = europe,
            locationmode = 'country names',
            locations = list(self.countries_fr_to_en.values()),
            z = values,
            text = text
        )])

        fig.update_geos(
            center=dict(lon=10, lat=55),
            resolution=50,
            showframe=False,
            visible=False,
            projection={
                "type": "mercator",
                "scale": 5
            },
        )

        fig.update_layout(
            title = "Ratio entre l'espérance de vie et le taux de " + name + " en Europe",
            margin = dict(l=140, r=140, t=50, b=50),
        )

        return fig

    def set_ratio_graph(self):
        fig = px.line(template='plotly_white')

        for country in self.countries:
            pollution_values = self.pollution.loc[self.pollution['country'] == country].reset_index(drop=True)
            particles_values = self.fine_particles.loc[self.fine_particles['country'] == country].reset_index(drop=True)
            lifespan_values = self.lifespan.loc[self.lifespan['country'] == country].reset_index(drop=True)
            
            pollution_ratios = lifespan_values.value.astype(float) / pollution_values.value.astype(float)
            particles_ratios = lifespan_values.value.astype(float) / particles_values.value.astype(float)

            fig.add_scatter(x = lifespan_values.year, y=pollution_ratios / particles_ratios, mode='lines', name=country, text=country, hoverinfo='x+y+text')

        xtitle = "Années"
        ytitle = "(taux pollution / espérance) / (taux particules fines / espérance)"
        fig.update_layout(
            title = 'Evolution du facteur entre l\'influence de la pollution et des particules fines sur l\'espérance de vie',
            xaxis = dict( title = xtitle,
                          type= 'linear',),
            yaxis = dict( title = ytitle,
                          type= 'linear',),
            height=450,
            hovermode='closest',
            legend = {'title': 'Pays'},
        )
        return fig
if __name__ == '__main__':
    plt = Impact()
    plt.app.run_server(debug=True, port=8051)
