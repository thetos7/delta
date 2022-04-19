import sys
import glob
import dash
import flask
import time
from dash import dcc
from dash import html
import pbmc_sujet.data.get_data as dp
import plotly.express as px

class Pbmc():     
        # Vehicle Types:
        # - PL - Poids Lourd
        # - VT - Véhicules Tourisme
        # - VU - Véhicules Utilitaires
        # - TC - Transport en Commun
        # - Moto lourde
        # - Moto légère
        # - Cyclo

        # Accident Types:
        # - mortel
        # - grave non mortel
        # - Léger

    def __init__(self, application = None):
        t_1 = time.time()
        df = dp.loadData()
        t_2 = time.time()
        print(f"Loaded database in {t_2 - t_1:.2f} seconds!")
        
        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de décès par jour en France'),
            html.Br(),
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )
        
        self.app = dash.Dash(__name__)
        self.app.layout = self.main_layout
    
    def show_hist():
        color = {
            "Léger" : "#FFFF00",
            "mortel" : "#FF0000",
            "grave non mortel" : "#FF7F00"
        }

        figure1 = px.histogram(
            df,
            x=df["Année"],
            color = df["Catégorie véhicule"],
            facet_col = "Type Accident",
            facet_col_wrap = 3,
        )

    def show_scatter():
        figure1.update_layout(barmode="stack", bargap=0.2)
        ddd = dp.getMortality(df)

        figure2 = px.scatter_3d(
            ddd,
            x = 'Année',
            y = 'Age véhicule',
            z = 'Count',
            color = 'Type Accident',
            color_discrete_map=color,
        )

if __name__ == '__main__':
    mpj = Pbmc()
    mpj.app.run_server(debug=True, port=8051)
