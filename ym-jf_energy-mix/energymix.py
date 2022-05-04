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

class EnergyMix():
    bcountries = ['Afghanistan','Africa', 'Albania', 'Algeria', 'American Samoa', 'Angola'
                'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Asia Pacific'
                'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh'
                'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan'
                'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil'
                'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi'
                'CIS', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands'
                'Central African Republic', 'Central America', 'Chad', 'Chile', 'China'
                'Colombia', 'Comoros', 'Congo', 'Cook Islands', 'Costa Rica', "Cote d'Ivoire"
                'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Czechoslovakia'
                'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica'
                'Dominican Republic', 'Eastern Africa', 'Ecuador', 'Egypt', 'El Salvador'
                'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Europe'
                'Europe (other)', 'Faeroe Islands', 'Falkland Islands ', 'Fiji', 'Finland'
                'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia'
                'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe'
                'Guam', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras'
                'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq'
                'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan'
                'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia'
                'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macau'
                'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Martinique'
                'Mauritania', 'Mauritius', 'Mexico', 'Middle Africa', 'Middle East', 'Moldova'
                'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar'
                'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles'
                'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue'
                'North America', 'North Korea', 'North Macedonia'
                'Northern Mariana Islands', 'Norway', 'OPEC', 'Oman', 'Other Asia & Pacific'
                'Other CIS', 'Other Caribbean', 'Other Middle East', 'Other Northern Africa'
                'Other South America', 'Other Southern Africa', 'Pakistan', 'Palestine'
                'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland'
                'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda'
                'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia'
                'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa'
                'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles'
                'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands'
                'Somalia', 'South & Central America', 'South Africa', 'South Korea'
                'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden'
                'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor'
                'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan'
                'Turks and Caicos Islands', 'USSR', 'Uganda', 'Ukraine'
                'United Arab Emirates', 'United Kingdom', 'United States'
                'United States Pacific Islands', 'United States Virgin Islands', 'Uruguay'
                'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam', 'Western Africa'
                'Western Sahara', 'World', 'Yemen', 'Yugoslavia', 'Zambia', 'Zimbabwe']

    def make_dataframe(self):
        energymix = pd.read_csv("./data/World_Energy_Consumption.csv", sep=",", skiprows=[], header=0)
        energymix = energymix.fillna(0.0)
        self.countries = energymix.country.unique()
        energymix = energymix.drop('iso_code' , axis=1)
        energymix = energymix.set_index('country')
        return energymix
    
    def __init__(self, application=None):
        self.energymix = self.make_dataframe()
        self.productions = self.energymix[['year', 'fossil_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity']]
        self.productions = self.productions[self.productions.year >= 1985]
        
        self.main_layout = html.Div(children=[
            html.H3(children='Mix énergétique de différents pays du monde'),
            html.Div([ dcc.Graph(id='graph1'), ], style={'width':'100%', }),
            html.Div([
                html.Div([ html.Div('Pays / Zone géographique'),
                           dcc.Dropdown(
                               id='graph1_countries',
                               options=self.countries,
                               value='France',
                               searchable=True,
                               clearable=False
                           )
                         ], style={'width': '9em'} )
                ], style={
                            'padding': '10px 50px', 
                            'display':'flex',
                            'flexDirection':'row',
                            'justifyContent':'flex-start',
                        }),
                html.Br(),
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
                    dash.dependencies.Output('graph1', 'figure'),
                    [ dash.dependencies.Input('graph1_countries', 'value')])(self.update_graph1)
        
    def update_graph1(self, country):
        fig = px.area(self.productions.loc[country], 'year', ['fossil_electricity', 'hydro_electricity', 'solar_electricity', 'wind_electricity', 'nuclear_electricity'],
            title = None,
                labels ={
                    "year": "Année",
                    "value": "Génération d'électricité en TW/h",
                    "variable": "Type de source"
                })
        return fig
        
if __name__ == '__main__':
    nrg = EnergyMix()
    nrg.app.run_server(debug=True, port=8051)