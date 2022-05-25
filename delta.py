import re
import dash
from dash import dcc
from dash import html
from energies import energies
from population import population
from deces import deces
from pbmc_accidents_routiers import pbmc_accidents_routiers as pbmc
from APTT_olympic import olympics
from YA_CDL_Energy_generation import Energy_generation
from EVHB_velib import velib
from kkhj_happinessPerceptionReality import happinessPerceptionReality
from mzgl_inegalites_de_revenus import mzgl_inegalites_de_revenus

from ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe import environment
from MDMR_NYPDCallsMeteoNY import NYPD_dash_visualisation as NYWeather

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
pop = population.WorldPopulationStats(app)
nrg = energies.Energies(app)
dec = deces.Deces(app)
pm = pbmc.Pbmc(app)
oly = olympics.Olympic(app)
eeg = Energy_generation.EuropeEnergyGeneration(app)
vel = velib.Velib(app)
hap = happinessPerceptionReality.HappinessPerceptionReality(app)
ine = mzgl_inegalites_de_revenus.Inegalites_de_revenus(app)

alvs = environment.EuropeanEnvironmentStudies(app)
nypd_weather = NYWeather.MDMR_NYPDCallsMeteoNY(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("Δelta δata")),
                              dcc.Link(html.Button("Prix d'énergies", style={'width':"100%"}), href='/energies'),
                              html.Br(),
                              dcc.Link(html.Button('Natalité vs revenus', style={'width':"100%"}), href='/pop'),
                              html.Br(),
                              dcc.Link(html.Button('MDMR_NYPDCallsMeteoNY', style={'width':"100%"}), href='/MDMR_NYPDCallsMeteoNY'),
                              html.Br(),
                              dcc.Link(html.Button('Décès journaliers', style={'width':"100%"}), href='/deces'),
                              html.Br(),
                              dcc.Link(html.Button('Accident Routiers', 
                                  style={'width':"100%", 'margin':0, 'padding': 0}), href='/accidents_routiers'),
                              dcc.Link(html.Button('Médailles Olympique', style={'width': "100%"}), href='/olympics'),
                              dcc.Link(html.Button("Génération d'énergie UE", style={'width':"100%"}), href='/Energy_generation'),
                              dcc.Link(html.Button('Utilisation Vélibs', style={'width':"100%"}), href='/EVHB_velib'),
                              dcc.Link(html.Button('Conception du bonheur', style={'width':"100%"}), href='/bonheur'),
                              dcc.Link(html.Button('Inégalités de revenus', style={'width':"100%"}), href='/inegalites'),
                              dcc.Link(html.Button('Politique et Environnement', style={'width':"100%"}), href='/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe'),
                              html.Br(),
                              html.Br(),
                              html.Br(),
                              html.Center(html.A('Code source', href='https://github.com/oricou/delta')),
                          ]),
                 html.Div(id='page_content', className="ten columns"),
            ]),
])


home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("Choisissez le jeu de données dans l'index à gauche."),
])

to_be_done_page = html.Div([
    dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
])

app.layout = main_layout

# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/energies':
        return nrg.main_layout
    elif pathname == '/pop':
        return pop.main_layout
    elif pathname == '/deces':
        return dec.main_layout
    elif pathname == '/accidents_routiers':
        return pm.main_layout
    elif pathname == '/olympics':
        return oly.main_layout
    elif pathname == '/Energy_generation':
        return eeg.main_layout
    elif pathname == '/EVHB_velib':
        return vel.main_layout
    elif pathname == '/bonheur':
        return hap.main_layout
    elif pathname == '/inegalites':
        return ine.main_layout
    elif pathname == '/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe':
        return alvs.main_layout
    elif pathname == '/MDMR_NYPDCallsMeteoNY':
        return nypd_weather.main_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
