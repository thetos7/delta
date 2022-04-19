import time
import pbmc_sujet.data.get_data as dp
import plotly.express as px
from dash import dcc
from dash import html

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
        if application:
            self.app = application
        t_1 = time.time()
        df = dp.loadData()
        t_2 = time.time()
        print("Loaded database in " + "{:.2f}".format(t_2 - t_1) + " seconds!")
    
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
