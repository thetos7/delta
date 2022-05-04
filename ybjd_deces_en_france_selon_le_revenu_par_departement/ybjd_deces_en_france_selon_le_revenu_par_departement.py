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
import datetime
import json

class DecesFranceRevenu():
    departements = json.load(open('ybjd_deces_en_france_selon_le_revenu_par_departement/data/departements-version-simplifiee.geojson'))

    def get_data(self):
        url_mort = "ybjd_deces_en_france_selon_le_revenu_par_departement/data/2022-01-28_deces_quotidiens_departement.xlsx"
        Excel_mort = pd.ExcelFile(url_mort)
        mort_france = pd.DataFrame({"Numéro département": [], "Nombre de morts": []})

        for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2A', '2B', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', 'France']:
            temp = pd.read_excel(Excel_mort, i).drop(columns=[
                "Nombre de décès quotidiens cumulés par département",
                "Unnamed: 1",
                "Unnamed: 2",
                "Unnamed: 3",
                "Unnamed: 4",
                "Unnamed: 5"
            ]).iloc[368]
            mort_france.loc[i] = [i, temp[0]]
        mort_france = mort_france.rename(index = {'France' : 'Total'})

        url_salaire = "https://www.insee.fr/fr/statistiques/fichier/2012717/TCRD_022.xlsx"
        Excel_salaire = pd.ExcelFile(url_salaire)

        salaire = pd.read_excel(Excel_salaire, 'DEP').rename(columns = {
            "Ménages fiscaux et revenu disponible en 2019 : comparaisons départementales": "Numéro département",
            'Unnamed: 1' : 'Département',
            'Unnamed: 2' : 'Nombre de ménages fiscaux',
            'Unnamed: 3' : 'Ménages fiscaux imposés (en %)',
            'Unnamed: 4' : 'Revenu médian'
        }).dropna().rename(index = {
            'M': 'Total'
        }).drop(columns=[
            'Unnamed: 5',
            'Unnamed: 6'
        ])
        salaire.drop([101, 102], axis=0, inplace=True)
        salaire['Numéro département'] = salaire['Numéro département'].replace(['M'], 'France')

        url_population = "ybjd_deces_en_france_selon_le_revenu_par_departement/data/estim-pop-dep-sexe-1975-2022.xlsx"
        Excel_population = pd.ExcelFile(url_population)
        population = pd.read_excel(Excel_population, 3).drop(columns = [
            "Unnamed: 2",
            "Unnamed: 3",
            "Unnamed: 4",
            "Unnamed: 5",
            "Unnamed: 6",
            "Unnamed: 8",
            "Unnamed: 9",
            "Unnamed: 10",
            "Unnamed: 11",
            "Unnamed: 12",
            "Unnamed: 13",
            "Unnamed: 14",
            "Unnamed: 15",
            "Unnamed: 16",
            "Unnamed: 17",
            "Unnamed: 18",
            "Unnamed: 19",
        ]).rename(columns = {
            "Estimation de population au 1er janvier, par département, sexe et grande classe d'âge" : "Numéro département",
            "Unnamed: 1" : "Département",
            "Unnamed: 7" : "Population"
        })
        population = population.drop([0, 1, 2, 3, 101, 102, 103, 104, 105, 106, 107, 108, 109])
        population.loc[100:100,'Numéro département':'Département'] = "France", "France métropolitaine"
        population = population.drop(["Département"], axis = 1)


        temp = pd.merge(population, mort_france, how = 'left', on = 'Numéro département')
        tot = pd.merge(temp, salaire, how = 'left', on='Numéro département')
        tot = tot[['Numéro département', 'Département', 'Population', 'Nombre de morts', 'Nombre de ménages fiscaux', 'Ménages fiscaux imposés (en %)', 'Revenu médian']]


        list = []
        for i in range (0, 97):
            list.append(100 * tot.iat[i, 3] / tot.iat[i, 2])
        tot['Pourcentage de morts'] = list

        list = []
        for i in range(0, 97):
            list.append(tot.iat[i, 6] / tot.iat[i, 3])
        tot['Revenu/Nombre de morts'] = list

        list = []
        for i in range(0, 97):
            list.append(int(tot.iat[i, 6] / tot.iat[i, 7]))
        tot['Revenu/Pourcentage de morts'] = list

        tot = tot[['Numéro département', 'Département', 'Population', 'Nombre de morts', 'Pourcentage de morts', 'Nombre de ménages fiscaux', 'Ménages fiscaux imposés (en %)', 'Revenu médian', 'Revenu/Nombre de morts', 'Revenu/Pourcentage de morts']]

        return tot

    def __init__(self, application = None):
        self.df = self.get_data()

        self.main_layout = html.Div(children=[
            html.H3(children='Décès en France selon le revenu par département'),
            html.Div([ dcc.Graph(id='drd-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='drd-value',
                                     options=[{'label':'Revenu/Pourcentage de morts', 'value':0},
                                              {'label':'Revenu/Nombre de morts', 'value':1}],
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
            html.Br(),
            dcc.Markdown("""
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
                dash.dependencies.Output('drd-main-graph', 'figure'),
                dash.dependencies.Input('drd-value', 'value'))(self.update_graph)


    def update_graph(self, value):
        if value == 0:
            fig = px.choropleth_mapbox(self.df,
                    geojson=self.departements,
                    locations='Numéro département',
                    featureidkey = 'properties.code',
                    color='Revenu/Pourcentage de morts',
                    color_continuous_scale="Viridis",
                    mapbox_style="carto-positron",
                    zoom=4.6, center = {"lat": 47, "lon": 2},
                    opacity=0.5,
                    labels={'Revenu/Pourcentage de morts':'Revenu/Pourcentage de morts'}
                    )
        else:
            fig = px.choropleth_mapbox(self.df,
                    geojson=self.departements,
                    locations='Numéro département',
                    featureidkey = 'properties.code',
                    color='Revenu/Nombre de morts',
                    color_continuous_scale="Viridis",
                    mapbox_style="carto-positron",
                    zoom=4.6, center = {"lat": 47, "lon": 2},
                    opacity=0.5,
                    labels={'Revenu/Nombre de morts':'Revenu/Nombre de morts'}
                    )

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return fig
        
if __name__ == '__main__':
    drd = DecesFranceRevenu()
    drd.app.run_server(debug=True, port=8051)
