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
"""
    departements = json.load(open('data/departements-version-simplifiee.geojson'))

    fig = px.choropleth_mapbox(prix_dep,#database ?
                           geojson=departements,#idem
                           locations='département',#idem ?
                           featureidkey = 'properties.code', # join keys #idem
                           color='prix',#colonne à afficher
                           color_continuous_scale="Viridis",#style couleur
                           mapbox_style="carto-positron",#idem au dessus
                           zoom=4.6, center = {"lat": 47, "lon": 2},
                           opacity=0.5,
                           labels={'prix':'Prix E10'}#nom barre à droite
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
"""

class DecesFranceRevenu():
    def get_data(self):
        url_mort = "data/2022-01-28_deces_quotidiens_departement.xlsx"
        Excel_mort = pd.ExcelFile(url_mort)
        mort_france = pd.DataFrame({"Numéro département": [], "Morts": []})

        for i in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2A', '2B', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', 'France']:
            mort_france.loc[i] = [i, pd.read_excel(Excel_mort, i).iat[368, 6]]

        mort_france = mort_france.set_index('Numéro département').rename(index = {'France' : 'Total'})
        url_salaire = "https://www.insee.fr/fr/statistiques/fichier/2012717/TCRD_022.xlsx"
        Excel_salaire = pd.ExcelFile(url_salaire)

        salaire = pd.read_excel(Excel_salaire, 'DEP').rename(columns = {
            "Ménages fiscaux et revenu disponible en 2019 : comparaisons départementales": "Numéro département",
            'Unnamed: 1' : 'Département',
            'Unnamed: 2' : 'Nombre de ménages fiscaux',
            'Unnamed: 3' : 'Ménages fiscaux imposés (en %)',
            'Unnamed: 4' : 'Revenu médian'
        }).set_index('Numéro département').drop(index = [
            '972',
            '974'
        ], columns = [
            'Unnamed: 5',
            'Unnamed: 6'
        ]).dropna().rename(index = {
            'M': 'Total'
        })


        tot = pd.merge(mort_france, salaire, how = 'left', on='Numéro département')
        tot = tot[['Département', 'Morts', 'Nombre de ménages fiscaux', 'Ménages fiscaux imposés (en %)', 'Revenu médian']]
        list = []
        for i in range (0, 97):
            list.append(tot.iat[i, 4] / tot.iat[i, 1])
        tot['revenu/morts'] = list
        return tot

    def __init__(self, application = None):
        #self.df = self.get_data()




        df = pd.concat([pd.read_pickle(f) for f in glob.glob('data/morts_par_jour-*')])
        df = df.groupby('deces').sum()
        df.sort_index(inplace=True)
        last_month = "02/2022"
        now = np.datetime64(datetime.datetime.now()).astype('datetime64[M]')
        df = df.loc['1973':now - np.timedelta64(2, 'M')]

        # calcul de la moyenne journalière avec des fenêtres
        # 2 passages pour retirer les valeurs qui dépassent l'écart type par rapport au sinus
        width = 10
        df2 = df.copy()
        for _ in range(2):
            prediction = pd.DataFrame({'x':np.zeros(len(df))}, index=df.index)
            prediction_nb = pd.DataFrame({'x':np.zeros(len(df))}, index=df.index)
            for step in range(1970, df.index[-1].year - width + 1):
                dfp = df2.loc[f'{step}':f'{step+width}']
                pente, v0 = np.polyfit(np.arange(len(dfp)), dfp.morts.values, 1)
                y = fft.fft(dfp.morts)
                y[y<30*len(dfp)] = 0
                pred = fft.ifft(y)
                pred -= dfp.morts.mean() - v0
                pred += np.cumsum([pente,]*len(dfp))
                prediction.loc[f'{step}':f'{step+width}', 'x'] += pred
                prediction_nb.loc[f'{step}':f'{step+width}','x'] += 1
            prediction = np.array([p.real for p in prediction.x]) / prediction_nb.x
            std = np.std(df.morts - prediction)
            df2.morts[df2.morts > prediction + std] = prediction.astype('int') + int(std)
            df2.morts[df2.morts < prediction - std] = prediction.astype('int') - int(std)
        del df2

        self.df = df
        self.day_mean = prediction




        self.main_layout = html.Div(children=[
            html.H3(children='Décès en France selon le revenu par département'),
            html.Div([ dcc.Graph(id='drd-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='drd-mean', 
                                     options=[{'label':'Courbe seule', 'value':0},
                                              {'label':'Courbe + Tendence générale', 'value':1}, 
                                              {'label':'Courbe + Moyenne journalière (les décalages au 1er janv. indique la tendence)', 'value':2}], 
                                     value=2,
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
                    dash.dependencies.Input('drd-mean', 'value'))(self.update_graph)

    def update_graph(self, mean):
        fig = px.line(self.df, template='plotly_white')
        fig.update_traces(hovertemplate='Bonjour', name='')
        fig.update_layout(
            xaxis = dict(title=""), 
            yaxis = dict(title="Salut"), 
            height=450,
            showlegend=False,
        )
        if mean == 1:
            reg = stats.linregress(np.arange(len(self.df)), self.df.morts)
            fig.add_scatter(x=[self.df.index[0], self.df.index[-1]], y=[reg.intercept, reg.intercept + reg.slope * (len(self.df)-1)], mode='lines', marker={'color':'red'})
        elif mean == 2:
            fig.add_scatter(x=self.df.index, y=self.day_mean, mode='lines', marker={'color':'red'})

        return fig

        
if __name__ == '__main__':
    drd = DecesFranceRevenu()
    drd.app.run_server(debug=True, port=8051)
