from statistics import mean
import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from .get_data import *
from urllib.request import urlopen
import json

axisX = html.Div(
    [
        html.Div("Catégorie"),
        dcc.RadioItems(
            id="pol-choice",
            options=[
                {"label": "Marque", "value": "Marque"},
                {
                    "label": "Hybride",
                    "value": "Hybride",
                },
                {"label": "Carburant", "value": "Carburant"},
            ],
            value="Marque",
            labelStyle={"display": "block"},
        ),
    ],
    style={"width": "9em", "padding": "0px 0px 0px 10em"},
)


class Pollution():

    def __init__(self, application=None):
        self.pollution_eu = get_transport_pollution_eu()
        self.pollution_vehicules_eu = get_pollution_per_vehicules_eu()
        self.pollution_vehicules_france = get_pollution_per_vehicules_in_france()
        self.pollution_schools_idf = get_air_pollution_schools()

        self.years = [x for x in range(1990, 2020)]
        self.pays = ['Allemagne', 'Autriche', 'Belgique', 'Bulgarie', 'Chypre',
                     'Croatie', 'Danemark', 'Espagne', 'Estonie', 'Finlande',
                     'France', 'Grèce', 'Hongrie', 'Irlande', 'Islande',
                     'Italie', 'Lettonie', 'Liechtenstein', 'Lituanie',
                     'Luxembourg', 'Malte', 'Norvège', 'Pays-Bas', 'Pologne',
                     'Portugal', 'Roumanie', 'Royaume-Uni', 'République Tchèque',
                     'Slovaquie', 'Slovénie', 'Suisse', 'Suède', 'Turquie']

        self.main_layout = html.Div(children=[
            html.H1(children="Pollution des Transports à différentes échelles"),
            html.Br(),
            html.H2(children='Étude de la pollution de l\'air en Europe'),
            html.H3(children='Pollution des Transports en Europe de 1990 à 2020'),
            html.Div([dcc.Graph(id='pol-main-europe-graph'), ],
                     style={'width': '100%'}),
            html.Div([
                html.Div([html.Div('Type de Pollution'),
                          dcc.RadioItems(
                    id='pol-europe-type',
                    options=[{'label': 'Oxyde d\'azote', 'value': "NOX"},
                         {'label': 'Composés organiques volatils autre que le méthane',
                             'value': "NMVOC"},
                         {'label': 'Particules < 10 nanomètres', 'value': "PM10"}],
                    value="NOX",
                    labelStyle={'display': 'block'},
                ), ]),
                html.Br(),
                html.Button(
                    'Start',
                    id='pol-button-start-stop',
                    style={'display': 'inline-block'}
                ),
                html.Div()

            ]),
            html.Div([
                html.Div(
                    dcc.Slider(
                        id='pol-europe-year-slider',
                        min=1990,
                        max=2020,
                        step=1,
                        value=1990,
                        marks={str(year): str(year)
                               for year in self.years[::2]},
                    ),
                    style={'display': 'inline-block', 'width': "90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='pol-auto-stepper',
                    interval=1500,       # in milliseconds
                    max_intervals=-1,  # start running
                    n_intervals=0
                ),
            ], style={
                'padding': '0px 50px',
                'width': '100%'
            }),
            html.Br(),
            html.H3(
                children="Émission de CO2 des véhicules neufs entre 2000 et 2020 en Europe"),
            html.Div([dcc.Graph(id="pol-europe-cars-graph")]),
            html.Div([
                html.Div([html.Div('Choix de visualisation'),
                          dcc.RadioItems(
                    id='pol-all-europe-choice',
                    options=[{'label': 'Un pays par rapport à toute l\'Europe', 'value': 'mean'},
                             {'label': 'Tous les pays', 'value': 'all_countries'}],
                    value='all_countries',
                    labelStyle={'display': 'block'},
                )], style={'width': '20em'}),
                html.Div([html.Div('Pays:'),
                          dcc.Dropdown(
                    id='pol-which-country',
                    options=[{'label': i, 'value': i}
                             for i in self.pays],
                    value='France',
                    disabled=True,
                ),
                ], style={'width': '15em', 'padding': '2em 0px 0px 0px'}),
                html.Div(style={'width': '2em'}),

            ], style={
                'padding': '25px 60px',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'flex-start',
            }),
            html.Br(),
            html.H2(children="Étude de la pollution des transports en France"),
            html.H3(
                children="Éjection de différents gaz en fonction de la marque en France en 2015"
            ),
            html.Div(
                [
                    dcc.Graph(id="pol-main-graph"),
                ],
                style={
                    "width": "100%",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Type de gaz"),
                            dcc.RadioItems(
                                id="pol-type-gaz",
                                options=[
                                    {"label": "Oxyde d'azote", "value": "NOx"},
                                    {
                                        "label": "Hydrocarbure et Oxyde d'azote",
                                        "value": "HC et NOx",
                                    },
                                    {"label": "Hydrocarbure", "value": "HC"},
                                    {
                                        "label": "Particules fine",
                                        "value": "Particules",
                                    },
                                    {"label": "CO2", "value": "CO2"},
                                    {"label": "CO type1", "value": "CO type1"},
                                ],
                                value="NOx",
                                labelStyle={"display": "block"},
                                #'Hybride', 'Carburant',
                            ),
                        ],
                        style={"width": "9em"},
                    ),
                    axisX,
                ],
                style={
                    "padding": "10px 50px",
                    "display": "flex",
                    "flexDirection": "row",
                    "justifyContent": "flex-start",
                },
            ),
            html.Br(),
            html.H3(
                children='Pollution aérienne des écoles et crêches en Île de France entre 2012 et 2017'),
            html.Br(),
            html.H2(children="À propos"),
            dcc.Markdown("""
                    * Sources :
                        * [Emissions de polluants des transports en Europe](https://ec.europa.eu/eurostat/databrowser/view/t2020_rk300/default/table?lang=fr)
                        * [Emissions de CO2 et de polluants des véhicules commercialisés en France] (https://www.data.gouv.fr/fr/datasets/emissions-de-co2-et-de-polluants-des-vehicules-commercialises-en-france/)
                        * [Base de données de la pollution aérienne aux abords des écoles et crèches d’Île-de-France] (https://www.data.gouv.fr/fr/datasets/base-de-donnees-de-la-pollution-aerienne-aux-abords-des-ecoles-et-creches-dile-de-france/)
                        * [Moyenne des émissions de CO2 par kilomètre provenant de véhicules particuliers neufs (source: AEE, DG CLIMA)] (https://ec.europa.eu/eurostat/databrowser/view/sdg_12_30/default/table?lang=fr)
                    * (c) 2022 Sarah Gutierez et Adrien Houpert
                        """),
            html.H3(children="")
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # European Pollution graph
        self.app.callback(
            dash.dependencies.Output('pol-main-europe-graph', 'figure'),
            [dash.dependencies.Input('pol-europe-type', 'value'),
             dash.dependencies.Input(
                'pol-europe-year-slider', 'value')
             ])(self.update_graph_poll_eu)

        # Button start/stop for europe map
        self.app.callback(
            dash.dependencies.Output('pol-button-start-stop', 'children'),
            dash.dependencies.Input('pol-button-start-stop', 'n_clicks'),
            dash.dependencies.State('pol-button-start-stop', 'children'))(self.button_on_click)
        self.app.callback(
            dash.dependencies.Output('pol-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('pol-button-start-stop', 'children')])(self.run_time)
        self.app.callback(
            dash.dependencies.Output('pol-europe-year-slider', 'value'),
            dash.dependencies.Input('pol-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('pol-europe-year-slider', 'value'),
             dash.dependencies.State('pol-button-start-stop', 'children')])(self.on_interval)

        # Callbacks for vehicules in EU
        self.app.callback(
            dash.dependencies.Output("pol-europe-cars-graph", "figure"),
            [
                dash.dependencies.Input("pol-all-europe-choice", "value"),
                dash.dependencies.Input('pol-which-country', 'value')
            ],
        )(self.update_graph_europe_cars)

        self.app.callback(
            [dash.dependencies.Output('pol-which-country', 'disabled'), ],
            dash.dependencies.Input('pol-all-europe-choice', 'value'))(self.disable_choice_country)
        # Callbacks for cars graph in France
        self.app.callback(
            dash.dependencies.Output("pol-main-graph", "figure"),
            [
                dash.dependencies.Input("pol-type-gaz", "value"),
                dash.dependencies.Input("pol-choice", "value"),
            ],
        )(self.update_graph_cars)

    def update_graph_europe_cars(self, all_europe='all_countries', country='France'):
        df, mean_eu = self.pollution_vehicules_eu

        if all_europe == 'mean':
            df = df.loc[df['Pays'] == country]
            # For all Europe we have data starting at 2007 
            min_year = 2007
            
            # BUT for certain countries the analysis starts later
            if df['Année'].min() > 2007:
                min_year = df['Année'].min()
                mean_eu = mean_eu.loc[mean_eu['Année'] >= min_year]

            mean_eu = pd.concat([mean_eu, df.loc[df['Année'] >= min_year]], ignore_index=True)
            fig = px.line(mean_eu, x='Année', y='Taux de pollution', color="Pays", title=f"Comparaison entre la moyenne des émissions de CO2 pour toute l\'Europe et en {country}")
            return fig

        return px.line(df, x='Année', y='Taux de pollution', color="Pays", title='Moyenne des émissions de CO2 pour chacun des pays d\'Europe')

    def update_graph_cars(self, name, axis):
        col = f"Emission {name}"
        agg = (
            self.pollution_vehicules_france.copy()[[axis, col]]
            .groupby([axis])
            .mean()
            .reset_index()
            .sort_values(by=[col, axis])
            # .replace(np.NaN,0)
        )

        fig = px.bar(
            agg, y=col, x=axis, title=f"Moyenne d'{col} pour les modèles par marque",
            color_discrete_sequence=['purple']*len(agg)
        )
        fig.update_traces(
            textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
        )
        return fig

    # Update function for the European map of pollution
    def update_graph_poll_eu(self, name="NMVOC", year=1990):
        dfg = self.pollution_eu[1]
        dfg = dfg.loc[dfg['Type de pollution'] == name]
        dfg = dfg.loc[dfg['Année'] == year]

        countries = json.load(
            open('SG_AH_pollution_des_transports/data/europe_geoson.json'))

        fig = px.choropleth_mapbox(dfg, geojson=countries,
                                   locations='Pays', featureidkey='properties.name',  # join keys
                                   color='Taux de pollution', color_continuous_scale="jet",
                                   mapbox_style="carto-positron",
                                   zoom=2.5, center={"lat": 53, "lon": 3},
                                   opacity=0.7,
                                   labels={
                                       'Taux de pollution': f'Poucentage de pollution de {name}'},
                                    range_color=[50,300]
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    # start and stop the time
    def button_on_click(self, n_clicks, text):
        if text == 'Start':
            return 'Stop'
        else:
            return 'Start'

    def run_time(self, text):
        if text == 'Start':
            return 0
        else:
            return -1

    # intervals for years
    def on_interval(self, n_intervals, year, text):
        if text == 'Stop':  # we run
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year

    # Enables of disables the poll for countries
    def disable_choice_country(self, info):
        return (info != 'mean',)


def transform_energ_names(df, col):
    energ_name = {
        "ES ": "Essence",
        "GO ": "Gazole",
        "ES/GP ": "Essence ou Gaz de Pétrole Liquéfié",
        "GP/ES ": "Essence ou Gaz de Pétrole Liquéfié",
        "EE ": "Essence Hybride rechargeable",
        "EL ": "Electricité",
        "EH ": "Essence Hybride non rechargeable",
        "GH ": "Gazole Hybride non rechargeable",
        "ES/GN ": "Essence ou Gaz Naturel",
        "GN/ES ": "Essence ou Gaz Naturel",
        "FE ": "Superéthanol",
        "GN ": "Gaz Naturel",
        "GL ": "Gazole Hybride rechargeable",
    }
    df[col].replace(energ_name, inplace=True)
    return df


if __name__ == "__main__":
    pol = Energies()
    pol.app.run_server(debug=True, port=8051)
