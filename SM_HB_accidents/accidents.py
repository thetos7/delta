import pandas as pd
import os
from dash import html
import glob

class Accidents():
    def __init__(self, application = None):
        #Ouvrir les csv
        #traitement préliminaire ?
        #concaténation en un seul dataframe
        # Jointure on Num_Acc
        
        #Dash integration
    """   
        self.main_layout = html.Div(children=[
            html.H3(children=['Contextualisation des accidents de la rotue'])])
        
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
    """            

if __name__ == '__main__':
    SMBH = Accidents()
    #SMBH.app.run_server(debug=True, port=8051)

