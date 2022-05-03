import pandas as pd
import os
from dash import html
import glob

class Accidents():
    def __init__(self, application = None):
        #Ouvrir les csv
        solver = {'voie' : 'O'}
        df_2015 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2015.csv")
        df_2016 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2016.csv", dtype=solver)
        df_2017 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2017.csv", dtype=solver)
        df_2018 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2018.csv", dtype=solver)
        df_2019 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2019.csv", sep=";")
        df_2020 = pd.read_csv("SM_HB_accidents/data/Lieux/lieux_2020.csv", sep=";")
        a = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2015.csv", encoding="latin-1")
        b = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2016.csv", encoding="latin-1")
        c = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2017.csv", encoding="latin-1")
        d = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2018.csv", encoding="latin-1")
        e = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2019.csv", sep=";")
        f = pd.read_csv("SM_HB_accidents/data/Caracteristiques/caracteristiques_2020.csv", sep=";")

        #traitement préliminaire ?
        #concaténation en un seul dataframe
        # Jointure on Num_Acc
        
        #Dash integration
        self.main_layout = html.Div(children=[
            html.H3(children=['Contextualisation des accidents de la route'])])
        
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

if __name__ == '__main__':
    SMBH = Accidents()
    #SMBH.app.run_server(debug=True, port=8051)

