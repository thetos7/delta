from kkhj_happinessPerceptionReality.getDatasets import get_datasets
from kkhj_happinessPerceptionReality.missingValues import *
from kkhj_happinessPerceptionReality.perceivedIndex import *
import dash
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objs as go
import plotly.express as px


class HappinessPerceptionReality():
    START = 'Start'
    STOP = 'Stop'

    def __init__(self, application=None):
        # Extract datasets
        datasets = get_datasets()

        # Store importance rates
        importanceRate = {'safety': 0.25,
                          'unemployment': 0.25,
                          'socialContribution': 0.25,
                          'gdpPerCapita': 0.25,
                          'educationLevel': 0}

        # Add perceived happiness
        datasets = add_perceived_index(datasets, importanceRate)

        # Initialise variables
        self.importanceRate = importanceRate
        self.df = datasets
        self.countries = get_countries_list(self.df)

        self.continent_colors = {'Asia': 'gold', 'Europe': 'green', 'Africa': 'red', 'Oceania': 'purple',
                                 'North America': 'blue', 'South America': 'pink'}
        self.french = {'Asia': 'Asie', 'Europe': 'Europe', 'Africa': 'Afrique', 'Oceania': 'Océanie',
                       'North America': 'Amérique du Nord', 'South America': 'Amérique du Sud'}
        self.years = sorted(set(self.df.index.values))

        self.main_layout = html.Div(children=[
            html.H3(children='Vrai Bonheur VS. Fake Bonheur'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'),

            html.Div([
                html.Div([dcc.Graph(id='wps-main-graphic'), ], style={'width': '80%'}),

                html.Div([
                    html.Div('Attributs'),
                    html.Label('PIB', htmlFor='gdp', style={'text-align': 'left',
                                                            'margin-right': '4px',
                                                            'display': 'inline-block',
                                                            'width': '55%'}),
                    dcc.Input(
                        name='gdp',
                        id='wps-attribute-ratio-gdp',
                        placeholder='',
                        type='number',
                        value=25,
                        style={'display': 'inline-block', 'width': '30%'}
                    ),
                    html.Br(),
                    html.Label('Chômage', htmlFor='unemployment', style={'text-align': 'left',
                                                                         'margin-right': '4px',
                                                                         'display': 'inline-block',
                                                                         'width': '55%'}),
                    dcc.Input(
                        name='unemployment',
                        id='wps-attribute-ratio-unemployment',
                        placeholder='Entrer une valeur pour le Chômage',
                        type='number',
                        value=25,
                        style={'display': 'inline-block', 'width': '30%'}
                    ),
                    html.Br(),
                    html.Label('Contribution Sociale', htmlFor='social-contribution', style={'text-align': 'left',
                                                                                            'margin-right': '4px',
                                                                                            'display': 'inline-block',
                                                                                            'width': '55%'}),
                    dcc.Input(
                        name='social-contribution',
                        id='wps-attribute-ratio-social-contribution',
                        placeholder='Entrer une valeur pour la contribution social',
                        type='number',
                        value=25,
                        style={'display': 'inline-block', 'width': '30%'}
                    ),
                    html.Br(),
                    html.Label('Sécurité', htmlFor='safety', style={'text-align': 'left',
                                                                    'margin-right': '4px',
                                                                    'display': 'inline-block',
                                                                    'width': '55%'}),
                    dcc.Input(
                        name='safety',
                        id='wps-attribute-ratio-safety',
                        placeholder='Entrer une valeur pour la sécurité',
                        type='number',
                        value=25,
                        style={'display': 'inline-block', 'width': '30%'}
                    ),

                    # TODO if education level, decomment line below
                    # html.Br(),
                    # html.Label('Éducation', htmlFor='education', style={'text-align': 'left',
                    #                                                     'margin-right': '4px',
                    #                                                     'display': 'inline-block',
                    #                                                     'width': '55%'}),
                    # dcc.Input(
                    #     name='education',
                    #     id='wps-attribute-ratio-education',
                    #     placeholder='Entrer une valeur pour l\'éducation',
                    #     type='number',
                    #     value=25,
                    #     style={'display': 'inline-block', 'width': '30%'}
                    # ),
                    html.Br(),
                    html.P('', style={'color': '#FF0000'}, id='wps-sum-message'),
                    html.Button('Calculer', id='wps-submit-button'),
                    html.Br(),
                    html.Br(),

                    html.Div('Continents'),
                    dcc.Checklist(
                        id='wps-crossfilter-which-continent',
                        options=[{'label': self.french[i], 'value': i} for i in sorted(self.continent_colors.keys())],
                        value=sorted(self.continent_colors.keys()),
                        labelStyle={'display': 'block'},
                    ),
                    html.Br(),
                    html.Button(
                        self.START,
                        id='wps-start-stop-button',
                        style={'display': 'inline-block'}
                    ),
                ], style={'margin-left': '15px', 'width': '15em', 'float': 'right'}),
            ], style={
                'padding': '10px 10px',
                'display': 'flex',
                'justifyContent': 'left'
            }),

            html.Div([
                html.Div(
                    dcc.Slider(
                        id='wps-year-slider',
                        min=self.years[0],
                        max=self.years[-1],
                        step=1,
                        value=self.years[0],
                        marks={str(year): str(year) for year in self.years[::1]},
                    ),
                    style={'display': 'inline-block', 'width': "90%"}
                ),
                dcc.Interval(  # fire a callback periodically
                    id='wps-stepper',
                    interval=500,  # in milliseconds
                    max_intervals=-1,  # start running
                    n_intervals=0
                ),
            ], style={
                'padding': '0px 10px',
                'width': '100%'
            }),

            html.Br(),
            html.Div(id='wps-country-div'),

            html.Div([
                dcc.Graph(id='wps-gdp-time-series',
                          style={'width': '25%', 'display': 'inline-block'}),
                dcc.Graph(id='wps-safety-time-series',
                          style={'width': '25%', 'display': 'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='wps-unemployment-time-series',
                          style={'width': '25%', 'display': 'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='wps-contribution-time-series',
                          style={'width': '25%', 'display': 'inline-block', 'padding-left': '0.5%'}),
                # TODO if educationLevel, decomment line below and change 25% to 20% in prev lines
                # dcc.Graph(id='wps-education-time-series',
                #           style={'width': '20%', 'display': 'inline-block', 'padding-left': '0.5%'}),
            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),

        ], style={
            # 'backgroundColor': 'rgb(240, 240, 240)',
            'padding': '10px 10px 10px 10px',
        }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # I link callbacks here since @app decorator does not work inside a class
        # (somhow it is more clear to have here all interaction between functions and components)
        self.app.callback(
            dash.dependencies.Output('wps-main-graphic', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-which-continent', 'value'),
             dash.dependencies.Input('wps-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('wps-country-div', 'children'),
            dash.dependencies.Input('wps-main-graphic', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('wps-start-stop-button', 'children'),
            dash.dependencies.Input('wps-start-stop-button', 'n_clicks'),
            dash.dependencies.State('wps-start-stop-button', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('wps-stepper', 'max_interval'),
            [dash.dependencies.Input('wps-start-stop-button', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('wps-year-slider', 'value'),
            dash.dependencies.Input('wps-stepper', 'n_intervals'),
            [dash.dependencies.State('wps-year-slider', 'value'),
             dash.dependencies.State('wps-start-stop-button', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('wps-gdp-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graphic', 'hoverData')])(self.update_gdp_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-safety-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graphic', 'hoverData')])(self.update_safety_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-unemployment-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graphic', 'hoverData')])(self.update_unemployment_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-contribution-time-series', 'figure'),
            [dash.dependencies.Input('wps-main-graphic', 'hoverData')])(self.update_contribution_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-sum-message', 'children'),
            [dash.dependencies.Input('wps-submit-button', 'n_clicks')],
            [dash.dependencies.State('wps-attribute-ratio-gdp', 'value')],
            [dash.dependencies.State('wps-attribute-ratio-safety', 'value')],
            [dash.dependencies.State('wps-attribute-ratio-unemployment', 'value')],
            [dash.dependencies.State('wps-attribute-ratio-social-contribution', 'value')], )(
            self.update_attributes_ratio)

    def update_attributes_ratio(self, n_clicks, v_gdp, v_safety, v_unemployment, v_contribution):
        if n_clicks:
            if v_gdp + v_safety + v_unemployment + v_contribution != 100:
                return "Sum needs to be equal to 100"
            else:
                self.importanceRate['gdpPerCapita'] = v_gdp / 100
                self.importanceRate['safety'] = v_safety / 100
                self.importanceRate['unemployment'] = v_unemployment / 100
                self.importanceRate['socialContribution'] = v_contribution / 100

                # TODO decomment line below if education defined
                # self.importanceRate['educationLevel'] = v_education

                self.df = add_perceived_index(self.df, self.importanceRate)

                return ""

    def update_graph(self, continents, year):
        dfg = self.df.loc[year]
        dfg = dfg[dfg['Continent'].isin(continents)]
        fig = px.scatter(dfg, x="Value", y="Perceived Happiness",
                         # title = f"{year}", cliponaxis=False,
                         size=None,
                         color="Continent", color_discrete_map=self.continent_colors,
                         hover_name="Country", log_x=True)
        fig.update_layout(
            xaxis=dict(title='Bonheur recueilli dans un sondage',
                       type='linear',
                       range=(0, 10)),
            yaxis=dict(title="Bonheur calculé", range=(0, 10)),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            hovermode='closest',
            showlegend=False,
        )
        return fig

    def get_country(self, hoverData):
        if hoverData is None:  # init value
            return self.df['Country'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    def create_time_series(self, country, what, title):
        return {
            'data': [go.Scatter(
                x=self.years,
                y=self.df[self.df["Country"] == country][what],
                mode='lines+markers',
            )],
            'layout': {
                'height': 300,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title': title,
                          'type': 'linear'},
                'xaxis': {'showgrid': False}
            }
        }

    # graph gdp vs years
    def update_gdp_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'GDP per capita', 'PIB par habitant en US $')

    # graph safety vs years
    def update_safety_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'Safety Index', "Sécurité (notée sur 10)")

    # graph unemployment vs years
    def update_unemployment_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'Unemployment Index', 'Chômage (noté sur 10)')

    # graph social contribution vs years
    def update_contribution_timeseries(self, hoverData):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'Social Security Employer Contribution Index',
                                       'Contribution sociale (notée sur 10)')

    # TODO if education, decomment the line below
    # # graph education vs years
    # def update_education_timeseries(self, hoverData):
    #     country = self.get_country(hoverData)
    #     return self.create_time_series(country, 'Education Level Index', 'Niveau d'éducation (noté sur 10)')

    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:  # then it means we are stopped
            return 0
        else:
            return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-1]:
                return self.years[0]
            else:
                return year + 1
        else:
            return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == "__main__":
    res = HappinessPerceptionReality()
    res.run(port=8055)
