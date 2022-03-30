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
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json


class Olympic():
    """mois = {'janv':1, 'févr':2, 'mars':3, 'avr':4, 'mai':5, 'juin':6, 'juil':7, 'août':8, 'sept':9, 'oct':10, 'nov':11, 'déc':12}

    quoi = {"Prix d'une tonne de propane":[1000, 'Propane'], "Bouteille de butane de 13 kg":[13, 'Butane'],
           "100 litres de FOD au tarif C1":[100, 'Fioul'], "Un litre d'essence ordinaire":[1, 'Essence'],
           "Un litre de super carburant ARS":[1, 'Essence'], "Un litre de super sans plomb 95":[1, 'Essence'],
           "Un litre de super sans plomb 98":[1, 'Essence'], "Un litre de gazole":[1, 'Gazole'],
           "Un litre de GPLc":[1, 'GPL'], "1 kWh (contrat 3 kW)":[1, 'Electricité'], "1 kWh (contrat 9 kW)":[1, 'Electricité'],
           "Une tonne de granulés de bois en vrac":[1000*4.8, 'Electricité'], "100 kWh PCI de bois en vrac":[100, 'Electricité']}

    densité =  {'Essence':0.75, 'Gazole':0.85, 'Fioul':0.85, 'GPL':0.55} # kg / l

    # https://fr.wikipedia.org/wiki/Pouvoir_calorifique
    calor = {'Essence':47.3, 'Gazole':44.8, 'Fioul':42.6, 'Propane':50.35, 'Butane':49.51, 'GPL':46, 'Bois':15, 'Charbon':20 ,
            'Electricité':3.6} # en MJ / kg sauf électicité en MJ / kWh
    """
    """
    def _conv_date(d):
        ma = d.split('-')                                      # coupe la chaine au - et ainsi ma[0] est le mois et ma[1] l'année
        return du.parser.parse(f"15-{Energies.mois[ma[0].lower()]}-{ma[1]}")  # parfois le mois a une majuscule d'où lower()
    """

    def _make_dataframe(filename):
        df = pd.read_csv(filename)
        df = df.drop(["City", "Sport", "Gender", "Athlete"], axis=1)
        df = df[df["Year"] >= 1918]
        df.drop(df.index[(df['Country'] == 'YUG') | (df['Country'] == 'TCH') | (df['Country'] == 'AHO') | (
                df['Country'] == 'EUN') | (df['Country'] == 'IOP') | (df['Country'] == 'IOA')], inplace=True)
        return df

    def __init__(self, application=None):
        summer = Olympic._make_dataframe("data/summer.csv")
        winter = Olympic._make_dataframe("data/winter.csv")

        self.olympic = pd.concat([summer, winter])

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de médailles olympiques par pays'),
            # html.Div([dcc.Graph(id='med-main-graph'), ], style={'width': '100%', }),
            html.Iframe(id="map", srcDoc=open('map.html', 'r').read(), width='100%', height='600'),
            html.Div([
                html.Div([html.Div('Medals'),
                          dcc.RadioItems(
                              id='med-spe',
                              options=[{'label': 'Marathon', 'value': 'Marathon'},
                                       {'label': '100M', 'value': '100M'}],
                              value='Marathon',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '9em'}),
                html.Div([html.Div('Event'),
                          dcc.Dropdown(
                              id='med-event',
                              options=['Marathon','100M'],
                              value=1,
                              disabled=False,
                          )]),
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
            })]
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('map', 'srcDoc'),
            [dash.dependencies.Input('med-spe', 'value'),
             dash.dependencies.Input('med-event', 'value')])(self.update_graph)

    def update_graph(self, med_type, name):
        event = self.olympic[self.olympic["Event"] == med_type]
        data = event["Country"].value_counts()
        df = pd.DataFrame.from_dict(data)
        df["ISO"] = list(df.index.values)
        fig = folium.Map(location=[28.5736, 9.0750], tiles=None, zoom_start=2, max_bounds=True, min_zoom=1)
        folium.Rectangle([(-20000, -20000), (20000, 20000)], fill=True, fill_color="#0080ff").add_to(fig)
        choro = folium.Choropleth(
            geo_data=f'data/countries.geojson',
            name='choropleth',
            data=df,
            columns=['ISO', 'Country'],
            key_on='feature.properties.ISO_A3',
            fill_color='RdPu',
            fill_opacity=1,
            line_opacity=0.8,
            Highlight=True,
            line_color='black',
            nan_fill_color="White",
            legend_name="Number of medals"
        ).add_to(fig)
        for c in choro.geojson.data['features']:
            if c['properties']['ISO_A3'] in df['ISO']:
                c['properties']['Medals'] = float(df.loc[c['properties']['ISO_A3'], 'Country'])
            else:
                c['properties']['Medals'] = 0
        folium.GeoJsonTooltip(['Country', 'Medals']).add_to(choro.geojson)
        folium.LayerControl().add_to(fig)
        fig.save("map.html")
        return open('map.html', 'r').read()


if __name__ == '__main__':
    nrg = Olympic()
    nrg.app.run_server(debug=True, port=8052)
