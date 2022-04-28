import numpy as np
import pandas as pd
import matplotlib
import glob
import plotly.express as px
from os import listdir
#Create dash application
import dash
from dash import Dash, dcc, html, Input, Output, State

class Cancer():
    #Store dataframes:
    def __init__(self, application = None):
        self.Africa = pd.read_pickle("cancer/data/Africa.pkl", compression="gzip")
        self.Asia = pd.read_pickle("cancer/data/Asia.pkl", compression="gzip")
        self.Europe = pd.read_pickle("cancer/data/Europe.pkl", compression="gzip")
        self.North_america = pd.read_pickle("cancer/data/North_america.pkl", compression="gzip")
        self.South_america = pd.read_pickle("cancer/data/South_america.pkl", compression="gzip")
        self.Oceania = pd.read_pickle("cancer/data/Oceania.pkl", compression="gzip")
        self.World = pd.read_pickle("cancer/data/World.pkl", compression="gzip")
        
        self.continent = ['Asia', 'Europe', 'Africa', 'Oceania', 
                                 'North-america', 'South-america']
        self.cancers = sorted(['Lip','Tongue','Mouth','Salivary glands','Tonsil','Oropharynx','Nasopharynx','Pyriform sinus','Hypopharynx','Oesophagus','Stomach','Small intestine','Colon','Rectosigmoid junction','Rectum','Anus','Liver','Gallbladder','Pancreas','Ill-defined digestive organs','Nasal cavity and middle ear','Accessory sinuses','Larynx','Trachea','Lung','Thymus','Heart, mediastinum and pleura','Bone','Skin','Mesothelioma','Kaposi sarcoma','Peripheral nerves', 'Peritoneum and retroperitoneum','Connective and soft tissue','Breast','Vulva','Vagina','Cervix uteri','Corpus uteri','Ovary','Other female genital organs','Placenta','Penis','Prostate','Other male genital organs','Kidney','Renal pelvis','Ureter','Bladder','Other urinary organs','Eye','Meninges', 'Central nervous system','Brain','Other parts of central nervous system','Thyroid','Adrenal gland','Other endoctrine','Non-Hodgkin lymphoma','Hodgkin disease',  'Immunoproliferative diseases','Multiple myeloma','Lymphoid leukaemia','Myeloid leukaemia','Leukaemia and unspecified','Myeloproliferative disorders','Myelodysplastic syndromes'])
        #Insérer la valeur du main layout représentant la page html elle même.
        #self.main_layout = None
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            #self.app.layout = self.main_layout

        app = Dash(__name__)

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des Cancers entre les pays'),
            html.Div([dcc.Graph(id='cancer-main-graph'), ], style={'width':'100%', }),
            dcc.RadioItems(
                            id='marginal-option-id',
                            options=[{'label': i, 'value': i} for i in ['violin', 'box']],
                            value='violin',
                            labelStyle={'display':'block'},
                        ),
            dcc.Checklist(
                            id='continent-id',
                            options=[{'label': i, 'value': i} for i in sorted(self.continent)],
                            value=[self.continent[1]],
                            labelStyle={'display':'block'},
                        ),
            dcc.Dropdown(
                            id='cancer-dropdown-id',
                            options=[{'label': i, 'value': i} for i in (self.cancers)],
                            value=['Lung'],
                            multi=True,
            )])
        

        self.app.callback(dash.dependencies.Output('cancer-main-graph','figure'),
                          dash.dependencies.Input('continent-id', 'value'),
                          dash.dependencies.Input('cancer-dropdown-id','value'),
                          dash.dependencies.Input('marginal-option-id','value'),
                          )(self.update_main_graph)
        
    def update_main_graph(self,continent_id,column_x,marginal_option):
        df = px.data.tips()
        sub_df= self.World[self.World['Continent'].isin(continent_id)]
        sub_df = sub_df[sub_df['Type of Cancer'].isin(column_x)]
        if marginal_option == 'violin' or marginal_option == 'box':
            fig = px.histogram(df, x=sub_df['Type of Cancer'],y=sub_df['Number of cases'],labels={'x':'Type of Cancer', 'y':'Number of cases'},marginal=marginal_option,text_auto=True)
        else:
            fig = px.histogram(df, x=sub_df['Type of Cancer'],y=sub_df['Number of cases'],labels={'x':'Type of Cancer', 'y':'Number of cases'},text_auto=True)
        return fig
    
    def update_graph(self, current_df, column_x, column_y, marginal_option):
        df = px.data.tips()
        if marginal_option == 'violin' or marginal_option == 'rug' or marginal_option == 'box':
            fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y],labels={'x':column_x, 'y':column_y,'color':column_color},marginal=marginal_option,text_auto=True)
        else:
            fig = px.histogram(df, x=current_df[column_x],y=current_df[column_y], color=current_df[column_color],labels={'x':column_x, 'y':column_y,'color':column_color},text_auto=True)
        return fig


if __name__ == '__main__':
    cncr = Cancer()
    cncr.app.run_server(debug=True,port=8051)