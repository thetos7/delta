import pandas as pd
import os
from dash import html

class Accidents():
    def __init__(self, application = None):

        filepaths = ["./data/" + f for f in os.listdir("./data/") 
                if f.endswith('.csv') and f.startswith('lieux')]
        df = pd.concat(map(lambda p: pd.read_csv(p, on_bad_lines='warn'), filepaths))
       

        #filepaths = ["./data/" + f for f in os.listdir("./data/") 
        #        if f.endswith('.csv') and f.startswith('caracteristiques')]
        #df_other = pd.concat(map(lambda p: pd.read_csv(p, on_bad_lines='skip'), filepaths))
        #df.set_index('Num_Acc').join(df_other.set_index('Num_Acc'))
        df.head()
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

