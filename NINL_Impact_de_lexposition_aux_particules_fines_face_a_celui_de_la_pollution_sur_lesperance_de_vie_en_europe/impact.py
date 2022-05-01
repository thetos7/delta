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

data_path = "NINL_Impact_de_lexposition_aux_particules_fines_face_a_celui_de_la_pollution_sur_lesperance_de_vie_en_europe/data/"
class Impact():
    def __init__(self, application = None):
        self.fine_particles = pd.read_pickle(data_path + "fine_particles_2008-2019.pkl")
        self.lifespan = pd.read_pickle(data_path + "lifespan_2006-2020.pkl")
        self.pollution = pd.read_pickle(data_path + "pollution_2008-2020.pkl")

        self.countries = np.intersect1d(self.fine_particles['country'], self.lifespan['country'])
        self.countries = np.intersect1d(self.countries, self.pollution['country'])

        self.main_layout = html.Div(children=[
            html.H3(children='Impact de l\'exposition aux particules fines face à celui de la pollution sur l\'espérance de vie en Europe'),
            html.Div([ dcc.Graph(id='imp-main-graph'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Prix'),
                           dcc.RadioItems(
                               id='imp-price-type',
                               options=[{'label':'Absolu', 'value':0}, 
                                        {'label':'Équivalent J','value':1},
                                        {'label':'Relatif : 1 en ','value':2}],
                               value=1,
                               labelStyle={'display':'block'},
                           )
                         ], style={'width': '9em'} ),
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
                En cliquant ou double-cliquant sur les lignes de la légende, vous choisissez les courbes à afficher.
                
                Notes :
                   * FOD est le fioul domestique.
                   * Pour les prix relatifs, seules les énergies fossiles sont prises en compte par manque de données pour les autres.
                   * Sources : 
                      * [base Pégase](http://developpement-durable.bsocom.fr/Statistiques/) du ministère du développement durable
                      * [tarifs réglementés de l'électricité](https://www.data.gouv.fr/en/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/) sur data.gouv.fr
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
                    dash.dependencies.Output('imp-main-graph', 'figure'),
                    dash.dependencies.Input('imp-price-type', 'value'))(self.update_graph)

    def update_graph(self, bjr):
        fig = px.line(template='plotly_white')
        for country in self.countries:
            country_values = self.pollution.loc[self.pollution['country'] == country]
            print(country_values)
            fig.add_scatter(x = country_values.year, y=country_values.value, mode='lines', name=country, text=country, hoverinfo='x+y+text')
        xtitle = "Années"
        ytitle = "Ratio pollution / particules fines"
        fig.update_layout(
            title = 'Evolution du ratio pollution / particules fines par pays',
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
