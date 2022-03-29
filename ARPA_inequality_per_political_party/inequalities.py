import dash
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from dash import dcc, html
from .data.get_data import extract_data

class Inequalities():
    START = 'Start'
    STOP  = 'Stop'

    def __init__(self, application = None):
        self.df = extract_data()
        self.color = {'gauche': 'red', 'centre': 'orange', 'droite': 'blue'}
        self.years = self.df.year.unique()

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des inéqualités par parti politique en Europe'),

            html.Div([
                    dcc.Graph(id='ine-main-graph'),
                ], style={
                    'display':'flex',
                    'justifyContent':'center'
                }),            
            
            html.Div([
                    html.Div(
                        dcc.Slider(
                                id='ine-crossfilter-year-slider',
                                min=self.years[0],
                                max=self.years[-1],
                                step = 1,
                                value=self.years[0],
                                marks={str(year): str(year) for year in self.years[::3]},
                        ),
                        style={'width':"50%"}
                    ),
                    dcc.Interval(            # fire a callback periodically
                        id='ine-auto-stepper',
                        interval=750,       # in milliseconds
                        max_intervals = -1,  # start running
                        n_intervals = 0
                    ),
                    html.Button(
                        self.START,
                        id='ine-button-start-stop', 
                    )
                ], style={
                    'display': 'flex',
                    'justifyContent':'center'
                })
        ])
        
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        
        self.app.callback(
            dash.dependencies.Output('ine-main-graph', 'figure'),
            [dash.dependencies.Input('ine-crossfilter-year-slider', 'value')])(self.update_graph)
        self.app.callback(
            dash.dependencies.Output('ine-button-start-stop', 'children'),
            dash.dependencies.Input('ine-button-start-stop', 'n_clicks'),
            dash.dependencies.State('ine-button-start-stop', 'children'))(self.button_on_click)
        # this one is triggered by the previous one because we cannot have 2 outputs for the same callback
        self.app.callback(
            dash.dependencies.Output('ine-auto-stepper', 'max_interval'),
            [dash.dependencies.Input('ine-button-start-stop', 'children')])(self.run_movie)
        # triggered by previous
        self.app.callback(
            dash.dependencies.Output('ine-crossfilter-year-slider', 'value'),
            dash.dependencies.Input('ine-auto-stepper', 'n_intervals'),
            [dash.dependencies.State('ine-crossfilter-year-slider', 'value'),
             dash.dependencies.State('ine-button-start-stop', 'children')])(self.on_interval)


    def update_graph(self, year):
        dfg = self.df[self.df.year == year]
        fig = px.scatter_geo(dfg, locations="iso", hover_name="country", hover_data=['gini'], scope='europe',
                             size="gini_display", color='color', color_discrete_sequence=["orange", "red", "blue"],
                             projection='natural earth')
        fig.update_geos(
            resolution=50,
            showcoastlines=True, coastlinecolor="RebeccaPurple",
            showland=True, landcolor="LightGreen",
            showocean=True, oceancolor="LightBlue",
        )
        fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
        return fig

    # start and stop the movie
    def button_on_click(self, n_clicks, text):
        if text == self.START:
            return self.STOP
        return self.START

    # this one is triggered by the previous one because we cannot have 2 outputs
    # in the same callback
    def run_movie(self, text):
        if text == self.START:    # then it means we are stopped
            return 0 
        return -1

    # see if it should move the slider for simulating a movie
    def on_interval(self, n_intervals, year, text):
        if text == self.STOP:  # then we are running
            if year == self.years[-1]:
                return self.years[0]
            return year + 1
        return year  # nothing changes

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)


if __name__ == '__main__':
    ineq = Inequalities()
    ineq.run(port=8055)