import glob
import json

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html


class Naissance():
    def __init__(self, application=None):

        with open('data/jcwg_departements.geojson') as f:
            dep = json.load(f)

        df = pd.concat(
            [pd.read_pickle(f) for f in glob.glob(
                'data/naissance-2019.pkl')])
        df.sort_index(inplace=True)

        self.date_axis = [pd.to_datetime(d) for d in sorted(set(
            df.index.values))]
        self.date = df.groupby(['DEPNAIS', 'date']).aggregate({
            'AGEMERE': np.mean,
            'AGEPERE': np.mean,
            'NBENF': np.mean,
            'SEXE': lambda x: sum(x == 1) / len(x),
        })
        self.date['SEXEG'] = 1 - self.date['SEXE']
        self.date['size'] = df.groupby(['DEPNAIS', 'date']).size()

        self.depnais = df.groupby('DEPNAIS').aggregate({
            'AGEMERE': np.mean,
            'AGEPERE': np.mean,
            'NBENF': np.mean,
            'SEXE': lambda x: sum(x == 1) / len(x),
        })
        self.depnais['size'] = df.groupby('DEPNAIS').size()

        agemere = df.groupby(['DEPNAIS', 'AGEMERE']).size().rename(
            'SIZEMERE')
        agepere = df.groupby(['DEPNAIS', 'AGEPERE']).size().rename(
            'SIZEPERE')

        self.age_pere_mere = pd.concat([agemere, agepere], axis=1)

        self.fig = go.Figure(go.Choroplethmapbox(
            geojson=dep,
            locations=self.depnais.index,
            z=self.depnais['size']
        ))

        self.fig.update_layout(mapbox_style="carto-positron",
                               mapbox_zoom=4.42,
                               mapbox_center={"lat": 47.0353, "lon": 2.2928},
                               margin={"r": 0, "t": 0, "l": 0, "b": 0},
                               hovermode='closest',
                               )

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de naissance par mois en France'),
            html.Div([
                dcc.Graph(id='map_france',
                          style={'width': '100%', 'display': 'inline-block'},
                          figure=self.fig)]),

            html.Br(),
            html.Div(id='sub_graph_department'),

            html.Div([
                dcc.Graph(id='number_of_child',
                          style={'width': '33%', 'display': 'inline-block'}),
                dcc.Graph(id='mean_parent_age',
                          style={'width': '33%', 'display': 'inline-block',
                                 'padding-left': '0.5%'}),
                dcc.Graph(id='child_sex',
                          style={'width': '33%', 'display': 'inline-block',
                                 'padding-left': '0.5%'}),
            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),
            html.Br(),
            dcc.Markdown("""
            Some text.
            """)
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

        # Subgraph of the map
        self.app.callback(
            dash.dependencies.Output('number_of_child', 'figure'),
            [dash.dependencies.Input('map_france', 'clickData'),
             ])(self.update_number_of_child)
        self.app.callback(
            dash.dependencies.Output('mean_parent_age', 'figure'),
            [dash.dependencies.Input('map_france', 'clickData'),
             ])(self.update_mean_parent_age)
        self.app.callback(
            dash.dependencies.Output('child_sex', 'figure'),
            [dash.dependencies.Input('map_france', 'clickData'),
             ])(self.update_child_sex)

    def get_department(self, hoverData):
        if hoverData is None:
            return '75'
        return hoverData['points'][0]['location']

    def update_number_of_child(self, clickData):
        department = self.get_department(clickData)
        return self.create_time_series(self.date, self.date_axis, department,
                                       [('size',
                                         '')],
                                       "Nombre d'enfants par mois")

    def update_mean_parent_age(self, clickData):
        department = self.get_department(clickData)
        return self.create_time_series(self.date, self.date_axis, department,
                                       [('AGEMERE', 'Age de la mère'),
                                        ('AGEPERE', 'Age du père')],
                                       "Age des parents à la naissance")

    def update_child_sex(self, clickData):
        department = self.get_department(clickData)
        return self.create_time_series(self.age_pere_mere, list(range(20, 46)),
                                       department,
                                       [('SIZEMERE', 'Mère'),
                                        ('SIZEPERE', 'Père')],
                                       "Nombre d'enfant par tranche d'age")

    def create_time_series(self, dataframe, x_axis, department, what, title):

        scatters = []
        for w, name in what:
            scatters.append(go.Scatter(
                x=x_axis,
                y=dataframe.loc[str(department)][w],
                name=name,
                mode='lines+markers',
            ))

        return {
            'data': scatters,
            'layout': {
                'height': 300,
                'margin': {'l': 50, 'b': 20, 'r': 10, 't': 20},
                'yaxis': {'title': title,
                          'type': 'linear'},
                'xaxis': {'showgrid': False}
            }
        }

    def update_subgraph(self, hoverData):
        tit = 'Nombre de naissance par jour'
        fig = px.line(self.df_age_pere_mere, template='plotly_white')
        tit = 'Difference d\'age entre le pere et la mere lors d\'une naissance'
        fig = px.line(self.df_evolution_age, template='plotly_white')
        tit = 'Evolution du nombre d\'enfant en fonction de l\'age des parents'
        fig = px.line(self.df_naissance, template='plotly_white')

        fig.update_traces(hovertemplate='%{y} naissance le %{x:%d/%m/%y}',
                          name='')
        fig.update_layout(
            # title = 'Évolution des prix de différentes énergies',
            xaxis=dict(title=""),  # , range=['2010', '2021']),
            yaxis=dict(title=tit),
            height=450,
            showlegend=False,
        )

        return fig


if __name__ == '__main__':
    mpj = Naissance()
    mpj.app.run_server(debug=True, port=8051)
