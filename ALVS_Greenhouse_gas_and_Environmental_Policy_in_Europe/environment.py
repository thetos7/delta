import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

class EuropeanEnvironmentStudies():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = pd.read_csv('ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe/data/europeanEnvTaxesPIB.csv')
        self.years = sorted(set(self.df.Time.values))
        self.pays = list(self.df.Pays.unique())
        self.main_layout = html.Div(children=[
            html.H3(children='Évolution des émissions de gaz à effet de serre selon les recettes fiscales environnementales'),

            html.Div('Déplacez la souris sur une bulle pour avoir les graphiques du pays en bas.'), 

            html.Div([
                    html.Div([ dcc.Graph(id='wps-main-graph-our'), ], style={'width':'90%', }),

                    html.Div([
                        html.Div('Pays'),
                        html.Div([
                        dcc.Checklist(
                            id='wps-crossfilter-which-pays',
                            options=[{'label': self.pays[i], 'value': self.pays[i]} for i in range(len(self.pays))],
                            value=sorted(self.pays),
                            labelStyle={'display':'block'},
                        )], style={'maxHeight':'300px', 'overflow':'scroll','width':'10em'}),
                        html.Br(),
                        html.Div('Échelle en X'),
                        dcc.RadioItems(
                            id='wps-crossfilter-xaxis-type',
                            options=[{'label': i, 'value': i} for i in ['Linéaire', 'Log']],
                            value='Linéaire',
                            labelStyle={'display':'block'},
                        ),
                        
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Button(
                            self.START,
                            id='wps-button-start-stop-our', 
                            style={'display':'inline-block'}
                        ),
                    ], style={'margin-left':'15px', 'width': '7em', 'float':'right'}),
                ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                html.Div(
                    dcc.Slider(
                            id='wps-crossfilter-year-slider-our',
                            min=self.years[0],
                            max=self.years[-1],
                            step = 1,
                            value=self.years[0],
                            marks={str(year): str(year) for year in self.years[::5]},
                    ),
                    style={'display':'inline-block', 'width':"90%"}
                ),
                dcc.Interval(            # fire a callback periodically
                    id='wps-auto-stepper-our',
                    interval=500,       # in milliseconds
                    max_intervals = -1,  # start running
                    n_intervals = 0
                ),
                ], style={
                    'padding': '0px 50px', 
                    'width':'100%'
                }),

            html.Br(),
            html.Div(id='wps-div-country-our'),

            html.Div([
                dcc.Graph(id='wps-income-time-series-our', 
                          style={'width':'33%', 'display':'inline-block'}),
                dcc.Graph(id='wps-fertility-time-series-our',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
                dcc.Graph(id='wps-pop-time-series-our',
                          style={'width':'33%', 'display':'inline-block', 'padding-left': '0.5%'}),
            ], style={ 'display':'flex', 
                       'borderTop': 'thin lightgrey solid',
                       'borderBottom': 'thin lightgrey solid',
                       'justifyContent':'center', }),
            
            
            
            
        ], style={
                #'backgroundColor': 'rgb(240, 240, 240)',
                 'padding': '10px 50px 10px 50px',
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
            dash.dependencies.Output('wps-main-graph-our', 'figure'),
            [ dash.dependencies.Input('wps-crossfilter-which-pays', 'value'),
              dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value'),
              dash.dependencies.Input('wps-crossfilter-year-slider-our', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('wps-div-country-our', 'children'),
            dash.dependencies.Input('wps-main-graph-our', 'hoverData'))(self.country_chosen)
        self.app.callback(
            dash.dependencies.Output('wps-button-start-stop-our', 'children'),
            dash.dependencies.Input('wps-button-start-stop-our', 'n_clicks'),
            dash.dependencies.State('wps-button-start-stop-our', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('wps-auto-stepper-our', 'max_interval'),
            [dash.dependencies.Input('wps-button-start-stop-our', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('wps-crossfilter-year-slider-our', 'value'),
            dash.dependencies.Input('wps-auto-stepper-our', 'n_intervals'),
            [dash.dependencies.State('wps-crossfilter-year-slider-our', 'value'),
             dash.dependencies.State('wps-button-start-stop-our', 'children')])(self.on_interval)
        self.app.callback(
            dash.dependencies.Output('wps-income-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_income_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-fertility-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_fertility_timeseries)
        self.app.callback(
            dash.dependencies.Output('wps-pop-time-series-our', 'figure'),
            [dash.dependencies.Input('wps-main-graph-our', 'hoverData'),
             dash.dependencies.Input('wps-crossfilter-xaxis-type', 'value')])(self.update_pop_timeseries)

    def update_graph(self, pays, xaxis_type, year):
        dfg = self.df[self.df.Time == year]
        dfg = dfg[dfg['Pays'].isin(pays)]
        fig = px.scatter(dfg, x = "PIB", y = "TAXES", 
                         #title = f"{year}", cliponaxis=False,
                         size = "T_HAB", size_max=40, 
                         color = "Pays", 
                         hover_name="Pays")
        fig.update_layout(
                 xaxis = dict(title='Pourcentage du PIB utilisé pour l\'environnement',
                              type= 'linear' if xaxis_type == 'Linéaire' else 'log',
                              range=(0,6) if xaxis_type == 'Linéaire' 
                                              else (np.log10(1), np.log10(10)) 
                             ),
                 yaxis = dict(title="Pourcentage des taxes pour l'environnement", range=(0,17)),
                 margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                 hovermode='closest',
                 showlegend=False,
             )
        return fig

    def create_time_series(self, country, what, axis_type, title):
        return {
            'data': [go.Scatter(
                x = self.years,
                y = self.df[self.df["Pays"] == country][what],
                mode = 'lines+markers',
            )],
            'layout': {
                'height': 225,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title':title,
                          'type': 'linear' if axis_type == 'Linéaire' else 'log'},
                'xaxis': {'showgrid': False}
            }
        }


    def get_country(self, hoverData):
        if hoverData == None:  # init value
            return self.df['Pays'].iloc[np.random.randint(len(self.df))]
        return hoverData['points'][0]['hovertext']

    def country_chosen(self, hoverData):
        return self.get_country(hoverData)

    # graph incomes vs years
    def update_income_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'T_HAB', xaxis_type, 'T_HAB')

    # graph children vs years
    def update_fertility_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'PIB', xaxis_type, "PIB")

    # graph population vs years
    def update_pop_timeseries(self, hoverData, xaxis_type):
        country = self.get_country(hoverData)
        return self.create_time_series(country, 'TAXES', xaxis_type, 'TAXES')

       # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        else:
            return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
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


if __name__ == '__main__':
    ws = EuropeanEnvironmentStudies()
    ws.run(port=8055)

