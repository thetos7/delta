import glob
import json

import dash
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
        self.dep2 = df.groupby('DEPDOM').size().reset_index()

        self.fig = go.Figure(go.Choroplethmapbox(
            geojson=dep,
            locations=self.dep2.DEPDOM,
            z=self.dep2[0]
        ))

        self.fig.update_layout(mapbox_style="carto-positron",
                               mapbox_zoom=4.42,
                               mapbox_center={"lat": 47.0353, "lon": 2.2928},
                               margin={"r": 0, "t": 0, "l": 0, "b": 0},
                               hovermode='closest',
                               )

        self.df_naissance = df.groupby('date').size()
        self.df_age_pere_mere = df.groupby('date').mean()[
            ['AGEMERE', 'AGEPERE']]

        d_mere = df.groupby('AGEMERE').size().rename('AGEMERE')
        d_pere = df.groupby('AGEPERE').size().rename('AGEPERE')
        self.df_evolution_age = pd.concat([d_mere, d_pere], axis=1)

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de naissance par mois en France'),
            html.Div(
                dcc.Graph(id='main-graph',
                          style={'width': '100%', 'display': 'inline-block'}),
            ),
            html.Div([
                dcc.Graph(id='wps-income-time-series',
                          style={'width': '100%', 'display': 'inline-block'},
                          figure=self.fig)]),
            html.Div(
                dcc.Graph(id='second_graph',
                          style={'width': '33%', 'display': 'inline-block'}),
            ),
            html.Div([dcc.RadioItems(id='mpj-choice',
                                     options=[
                                         {'label': 'Naissance par mois',
                                          'value': 0},
                                         {'label': 'Age moyen pere/mere',
                                          'value': 1},
                                         {'label': 'Evolution age parents',
                                          'value': 2}],
                                     value=0,
                                     labelStyle={'display': 'block'}),
                      ]),
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

        self.app.callback(
            dash.dependencies.Output('main-graph', 'figure'),
            dash.dependencies.Input('mpj-choice', 'value'))(self.update_graph)

        self.app.callback(
            dash.dependencies.Output('second_graph', 'figure'),
            [dash.dependencies.Input('wps-income-time-series', 'hoverData'),
             ])(self.update_subgraph)

    def update_subgraph(self, hoverData):
        print(hoverData)
        return None

    def update_graph(self, choice):
        tit = 'Nombre de naissance par jour'
        if choice == 1:
            fig = px.line(self.df_age_pere_mere, template='plotly_white')
            tit = 'Difference d\'age entre le pere et la mere lors d\'une naissance'
        elif choice == 2:
            fig = px.line(self.df_evolution_age, template='plotly_white')
            tit = 'Evolution du nombre d\'enfant en fonction de l\'age des parents'
        else:
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

        print("Done3", choice)
        return fig

if __name__ == '__main__':
    mpj = Naissance()
    mpj.app.run_server(debug=True, port=8051)
