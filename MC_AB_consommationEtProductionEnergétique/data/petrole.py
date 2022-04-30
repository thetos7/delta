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

from get_data import get_data
from get_data import get_by_year
from get_data import list_years


class Independance_Petrole():
    def __init__(self, application=None):

        prod_cons, export, impor = get_data()

        
        years = list_years(impor)
        print(years)

        self.main_layout = html.Div(children=[
            html.H3(children='Petrole'),
            dcc.Markdown("""Independance Européene face au Petrole comme energie fossile"""),
            html.Div([ html.Div('Année ref.'),
                          dcc.Dropdown(
                               id='nrg-which-year',
                               options=[{'label': i, 'value': i} for i in years],
                               value=1,
                               disabled=False,
                           ),
                         ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
        #html.Div([ dcc.Graph(id='nrg-main-graph'), ], style={'width':'100%', }),
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
    
    def update_graph(self, price_type, month, year, xaxis_type):
        if price_type == 0 or month == None or year == None:
            df = self.energie
        elif price_type == 1:
            df = self.energie.copy()
            for c in df.columns:
                alias = Energies.quoi[c][1]
                try:
                    df[c] = df[c] / (Energies.quoi[c][0] * Energies.densité[alias] * Energies.calor[alias])
                except:  # l'unité est déjà en kg et donc densité n'existe pas
                    df[c] = df[c] / (Energies.quoi[c][0] * Energies.calor[alias])
        else:
            df = self.petrole.copy()
            df /= df.loc[f"{year}-{month}-15"]
        fig = px.line(df[df.columns[0]], template='plotly_white')
        for c in df.columns[1:]:
            fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c, hoverinfo='x+y+text')
        ytitle = ['Prix en €', 'Prix en € pour 1 mégajoule', 'Prix relative (sans unité)']
        fig.update_layout(
            #title = 'Évolution des prix de différentes énergies',
            yaxis = dict( title = ytitle[price_type],
                          type= 'linear' if xaxis_type == 'Linéaire' else 'log',),
            height=450,
            hovermode='closest',
            legend = {'title': 'Énergie'},
        )
        return fig



if __name__ == '__main__':
    ind = Independance_Petrole()
    ind.app.run_server(debug=True, port=8051)
