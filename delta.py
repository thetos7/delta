import re
#from this import d
import dash
import flask
from dash import dcc
from dash import html
from energies import energies
from population import population
from deces import deces
from MC_AB_consommationEtProductionEnergétique import petrole
from SG_AH_pollution_des_transports import pollution
from pbmc_accidents_routiers import pbmc_accidents_routiers as pbmc
from APTT_olympic import olympics
from YA_CDL_Energy_generation import Energy_generation
from EVHB_velib import velib
from kkhj_happinessPerceptionReality import happinessPerceptionReality
from mzgl_inegalites_de_revenus import mzgl_inegalites_de_revenus
from ARPA_inequality_per_political_party import inequalities
from ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe import environment
from MDMR_NYPDCallsMeteoNY import NYPD_dash_visualisation as NYWeather
from ABNZ_Pollution_aux_US_et_corrélation_avec_le_prix_du_carburant import pollution
from phllhlv_emissionglobalwarming import global_warming
from tdmr_quality_of_life_and_worktime import tdmr_quality_of_life_and_worktime as tdmr
from strl_EvolutionDesSalairesAnnuelsMoyens import income
from cerg_cancer import cancer
from ACJW_MusicPopularityFactor import Music
from RCNT_sujetTelevise import sujetTelevise
from ym_jf_energy_mix import energymix
from afhy_electricite import electricite
from NINL_Impact_de_lexposition_aux_particules_fines_face_a_celui_de_la_pollution_sur_lesperance_de_vie_en_europe import impact
from ps_ap_chessgames.src import chess
from JD_NJ_Etude_de_la_pollution import dash_app_pollution
from ybjd_deces_en_france_selon_le_revenu_par_departement import ybjd_deces_en_france_selon_le_revenu_par_departement as ybjd
from TA_MG_SpotifyMusicPopularity import spotify
from aa_sc_metacritic import metacritic
from TBGP_salaires_inflation import app as tbgp_si_lib
from jcwg_naissance_deces import naissance_deces
from YBYB_Analyse_football import football
from avel_top_100_billboard_usa import top_100_billboard_usa
from abih import abih
from TBGT_population_vs_train_speed import TBGT_population_vs_train_speed as tbgt_lib
from postbac import postbac
from presidentielle import presidentielle
from EC_CD_Evolution_des_Mariages_en_France import mariages_en_France as md_lib

#@profile
def init():
    app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
    pop = population.WorldPopulationStats(app)
    dec = deces.Deces(app)
    nrg = energies.Energies(app)
    pm =  dec # pbmc.Pbmc(app)
    oly = olympics.Olympic(app)
    eeg = Energy_generation.EuropeEnergyGeneration(app)
    vel = velib.Velib(app)
    hap = dec # happinessPerceptionReality.HappinessPerceptionReality(app)
    ine_rev = mzgl_inegalites_de_revenus.Inegalites_de_revenus(app)
    alvs = environment.EuropeanEnvironmentStudies(app)
    nypd_weather = NYWeather.MDMR_NYPDCallsMeteoNY(app)
    globalwarming = global_warming.GlobalWarming(app)
    td = tdmr.Tdmr(app)
    pet = dec # petrole.Petrole(app)
    inc = income.Income(app)
    pol = pollution.Pollution(app)
    cncr = cancer.Cancer(app)
    mus = Music.Song(app)
    ine_gini = dec # inequalities.Inequalities(app)
    suj = sujetTelevise.TvSubject(app)
    nrgmix = energymix.EnergyMix(app)
    ele = electricite.Eletricite(app)
    imp = impact.Impact(app)
    chs = chess.Chess(app)
    pol = dash_app_pollution.PollutionFrancaise(app)
    drd = dec # ybjd.DecesFranceRevenu(app)
    spo = spotify.Spotify(app)
    meta = metacritic.Metacritic(app)
    tbgp_si = tbgp_si_lib.SalaryInflation(app)
    jcwg_nd = naissance_deces.Naissance(app)
    foot = football.Football(app)
    billboard = top_100_billboard_usa.Top100BillboardUSA(app)
    meteor = abih.Abih(app)
    tbgt = tbgt_lib.TBGT(app)
    psb = postbac.PostBac(app)
    pres = presidentielle.Presidentielles(app)
    md = md_lib.Mariage(app)

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
                                  dcc.Link(html.Button('Accident Routiers', style={'width':"100%", 'margin':0, 'padding': 0}), href='/accidents_routiers'),
                                  dcc.Link(html.Button('Médailles Olympique', style={'width': "100%"}), href='/olympics'),
                                  dcc.Link(html.Button("Génération d'énergie UE", style={'width':"100%"}), href='/Energy_generation'),
                                  dcc.Link(html.Button('Utilisation Vélibs', style={'width':"100%"}), href='/EVHB_velib'),
                                  dcc.Link(html.Button('Conception du bonheur', style={'width':"100%"}), href='/bonheur'),
                                  dcc.Link(html.Button('Inégalités de revenus', style={'width':"100%"}), href='/inegalites'),
                                  dcc.Link(html.Button('Politique et Environnement', style={'width':"100%"}), href='/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe'),
                                  dcc.Link(html.Button('Polutions/Pétroles', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Global Warming', style={'width':"100%"}), href='/global_warming'),
                                  dcc.Link(html.Button('impact temps de travail', style={'width':"100%", 'padding':'inherit'}), href='/travail'),
                                  dcc.Link(html.Button('Pétrole en Europe', style={'width':"100%"}), href='/petrole'),
                                  dcc.Link(html.Button('Evolution des salaires', style={'width':"100%", 'padding':'inherit'}), href='/salaires'),
                                  dcc.Link(html.Button('Pollution des transports', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Répartition des cancers', style={'width':"100%"}), href='/cancer'),
                                  dcc.Link(html.Button('Popularité des musiques', style={'width':"100%"}), href='/music'),
                                  dcc.Link(html.Button('Inégalités en Europe', style={'width':"100%"}), href='/inequality'),
                                  dcc.Link(html.Button('Sujet tv', style={'width':"100%"}), href='/sujetTV'),
                                  dcc.Link(html.Button('Electricité monde', style={'width':"100%"}), href='/energymix'),
                                  dcc.Link(html.Button("Électricité", style={'width':"100%"}), href='/electricite'),
                                  dcc.Link(html.Button('Espérance de vie vs pollution', style={'width':"100%"}), href='/impact'),
                                  dcc.Link(html.Button("Parties d'échecs", style={"width": "100%"}), href="/chess"),
                                  dcc.Link(html.Button('Etude de la pollution', style={'width':"100%"}), href='/pollution'),
                                  dcc.Link(html.Button('Décès selon le revenu', style={'width':"100%"}), href='/ybjd_deces_en_france_selon_le_revenu_par_departement'),
                                  dcc.Link(html.Button('Popularité des musiques', style={'width':"100%"}), href='/spotify'),
                                  dcc.Link(html.Button('Analyse Metacritic', style={'width':"100%"}), href='/aa_sc_metacritic'),
                                  dcc.Link(html.Button('Salaires / inflation', style={'width':"100%"}), href='/tbgp-salaires-inflation'),
                                  dcc.Link(html.Button('Naissances et décès', style={'width':"100%"}), href='/jcwg_naissance_deces'),
                                  dcc.Link(html.Button("Football Classement, Age, €", style={'width':"100%"}), href='/football'),
                                  dcc.Link(html.Button('Top 100 Billboard USA', style={'width':"100%"}), href='/usa_billboard'),
                                  dcc.Link(html.Button('Les météorites', style={'width':"100%"}), href='/meteor'),
                                  dcc.Link(html.Button('Population vs Grandes Lignes', style={'width':"100%", 'margin':0, 'padding': 0}), href='/population_vs_train_speed'),
                                  dcc.Link(html.Button('Education test', style={'width':"100%"}), href='/postbac'),
                                  dcc.Link( html.Button('Présidentielle', style={'width': "100%", 'margin-bottom': '5px'}), href='/presidentielle'),
                                  dcc.Link(html.Button('Mariages', style={'width':"100%"}), href='/EC_DC_Evolution_des_Mariages_en_France'),
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

    # "complete" layout (not sure that I need that)
    app.validation_layout = html.Div([
        main_layout,
        to_be_done_page,
        pop.main_layout,
    ])

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
            return ine_rev.main_layout
        elif pathname == '/ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe':
            return alvs.main_layout
        elif pathname == '/MDMR_NYPDCallsMeteoNY':
            return nypd_weather.main_layout
        elif pathname == '/pollution':
            return pol.main_layout
        elif pathname == '/global_warming':
            return globalwarming.main_layout
        elif pathname == '/travail':
            return td.main_layout
        elif pathname == '/petrole':
            return pet.main_layout
        elif pathname == '/salaires':
            return inc.main_layout
        elif pathname == '/pollution':
            return pol.main_layout
            return dec.main_layout 
        elif pathname == '/cancer':
            return cncr.main_layout
        elif pathname == '/music':
            return mus.main_layout
        elif pathname == '/inequality':
            return ine_gini.main_layout
        elif pathname == '/sujetTV':
            return suj.main_layout
        elif pathname == '/energymix':
            return nrgmix.main_layout
        elif pathname == '/electricite':
            return ele.main_layout
        elif pathname == '/impact':
            return imp.main_layout
        elif pathname == "/chess":
            return chs.main_layout
        elif pathname == "/pollution" :
            return pol.main_layout
        elif pathname == '/ybjd_deces_en_france_selon_le_revenu_par_departement':
            return drd.main_layout
        elif pathname == '/spotify':
            return spo.main_layout
        elif pathname == '/aa_sc_metacritic':
            return meta.main_layout
        elif pathname == '/tbgp-salaires-inflation':
            return tbgp_si.main_layout
        elif pathname == '/jcwg_naissance_deces':
            return jcwg_nd.main_layout
        elif pathname == '/football':
            return foot.main_layout
        elif pathname == '/usa_billboard':
            return billboard.main_layout
        elif pathname == '/meteor':
            return meteor.main_layout
        elif pathname == '/population_vs_train_speed':
            return tbgt.main_layout
        elif pathname == '/postbac':
            return psb.main_layout
        elif pathname == '/presidentielle':
            return pres.main_layout
        elif pathname == '/EC_DC_Evolution_des_Mariages_en_France' :
            return md.main_layout
        else:
            return home_page
    return app

app = init()
server = app.server

if __name__ == '__main__':
    profile = False
    if not profile:
        app.run_server(debug=True)
