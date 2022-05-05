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
            self.dep = json.load(f)

        # Load pkl
        self.daten = pd.read_pickle('data/date_naissance.pkl')
        self.dated = pd.read_pickle('data/date_deces.pkl')

        self.depn = pd.read_pickle('data/department_naissance.pkl')
        self.depd = pd.read_pickle('data/department_deces.pkl')

        self.agen = pd.read_pickle('data/age_naissance.pkl')
        self.aged = pd.read_pickle('data/age_deces.pkl')

        self.zmax = max(self.depn['SIZE'].max(), self.depd['SIZE'].max())
        self.zmin = min(self.depn['SIZE'].min(), self.depd['SIZE'].min())

        # Set info for graph
        self.tickval = [self.zmin, 1000, 2000, 5000, 10000, 20000, 30000,
                        self.zmax]
        self.date_axis = [pd.to_datetime(d) for d in sorted(set(
            self.daten.reset_index()['date']))]
        self.age_naissances_axis = list(range(17, 46))
        self.age_deces_axis = list(sorted(set(self.aged.reset_index()['AGE'])))
        self.dep_map = {d['properties']['code']: d['properties']['nom']
                        for d in self.dep['features']}

        self.fign = self.fig_naissance()
        self.figd = self.fig_deces()

        # main layout
        self.main_layout = html.Div(children=[
            html.H3(children='Naissance et décès en France en 2019'),
            html.Div([
                html.Div([
                    dcc.Graph(id='map_france_naissance',
                              figure=self.fign,
                              style={'width': '100%',
                                     'display': 'inline-block'}, ),
                ], style={'width': '50%'}, ),
                html.Div([
                    dcc.Graph(id='map_france_deces',
                              figure=self.figd,
                              style={'width': '100%',
                                     'display': 'inline-block',
                                     'padding-left': '0.5%'}, ),
                ], style={'width': '50%'}, ),
            ],
                style={
                    'display': 'flex',
                    'justifycontent': 'center',
                }
            ),

            html.Div([
                html.Plaintext(id='list_department_naissance',
                               style={
                                   'width': '50%',
                                   'whiteSpace': 'normal',
                                   'height': 'auto',
                                   'overflow-wrap': 'break-word',
                               }),
                html.Plaintext(id='list_department_deces',
                               style={
                                   'width': '50%',
                                   'whiteSpace': 'normal',
                                   'height': 'auto',
                                   'overflow-wrap': 'break-word',
                               }),
            ],
                style={
                    'display': 'flex',
                    'justifycontent': 'center',
                    'height': 'auto',
                }
            ),

            html.Br(),
            html.Div([
                dcc.Graph(id='size_france',
                          style={'width': '95%', 'display': 'inline-block'}),
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-naissance-deces-1',
                        options=[{'label': i, 'value': i} for i in
                                 ['Naissance', 'Décès']],
                        value=['Naissance', 'Décès'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-1',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block'}),
            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),
            html.Br(),
            html.Div([
                dcc.Graph(id='size_naissance',
                          style={'width': '90%', 'display':
                              'inline-block', }),
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-hf-2',
                        options=[{'label': i, 'value': i} for i in
                                 ['Femme', 'Homme', 'Somme', 'Moyenne']],
                        value=['Femme', 'Homme'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-2',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block', }),

                dcc.Graph(id='size_deces',
                          style={'width': '90%',
                                 'display': 'inline-block', }),
                html.Div([
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    dcc.Checklist(
                        id='wps-hf-3',
                        options=[{'label': i, 'value': i} for i in
                                 ['Femme', 'Homme', 'Somme', 'Moyenne']],
                        value=['Femme', 'Homme'],
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                    html.Br(),
                    dcc.RadioItems(
                        id='wps-uni-mg-3',
                        options=[{'label': i, 'value': i} for i in
                                 ['Unitaire', 'Moyenne', ]],
                        value='Moyenne',
                        labelStyle={'display': 'block', 'font-size': 12},
                    ),
                ], style={'width': '10%', 'display': 'inline-block'}),

            ], style={'display': 'flex',
                      'borderTop': 'thin lightgrey solid',
                      'borderBottom': 'thin lightgrey solid',
                      'justifyContent': 'center', }),
            html.Br(),
            dcc.Markdown("""
            Les cartes sont interactifs. En passant la souris sur les départements vous avez une infobulle.
            De plus, en séléctionnant plusieurs départements (shift et click), on peut avoir plus d'info sur ceux-ci à l'aide des graphiques.
            En utilisant les icônes en haut à droite, on peut agrandir une zone, déplacer la carte, réinitialiser avec d'un double click et utiliser le lasso pour sélectionner plusieurs départements.

            #### Informations intéressantes :
               * On remarque que les grosses villes ont un important nombre de naissance et un plus faible nombre de décès.
                Avec l'age les gens finnissent leur vie en régions plutôt que dans les grandes villes.
               * Cela se confirme en étudiant les départements unitairement, les zones à forte population ont plus de naissance que de décès.
                On observe le phénomène inverse dans les départements moins peuplés.
               * On observe une croissance démographique en France, il y a plus de naissance que de décès.
               * On repère les hivers avec un nombre plus important de mort durant ces périodes. 
               * On observe moins de naissance de février à avril, pour un pic de naissance en juillet.
               * Les hommes ont en moyenne des enfants plus tard que les femmes.
               * Les femmes vivent plus longtemps que les hommes

            #### À propos

            * Sources : https://www.data.gouv.fr/fr/datasets/population/
            * (c) 2022 William Grolleau, Jeremy Croiset.
            """)
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        # Subgraph of the map
        self.app.callback(
            dash.dependencies.Output('size_france', 'figure'),
            [dash.dependencies.Input('map_france_naissance', 'selectedData'),
             dash.dependencies.Input('map_france_deces', 'selectedData'),
             dash.dependencies.Input('wps-naissance-deces-1', 'value'),
             dash.dependencies.Input('wps-uni-mg-1', 'value'),
             ])(self.size_france)
        self.app.callback(
            dash.dependencies.Output('size_naissance', 'figure'),
            [dash.dependencies.Input('map_france_naissance', 'selectedData'),
             dash.dependencies.Input('wps-uni-mg-2', 'value'),
             dash.dependencies.Input('wps-hf-2', 'value'),
             ])(self.size_naissance)
        self.app.callback(
            dash.dependencies.Output('size_deces', 'figure'),
            [dash.dependencies.Input('map_france_deces', 'selectedData'),
             dash.dependencies.Input('wps-uni-mg-3', 'value'),
             dash.dependencies.Input('wps-hf-3', 'value'),
             ])(self.size_deces)

        self.app.callback(
            dash.dependencies.Output('map_france_deces', 'figure'),
            [dash.dependencies.Input('map_france_naissance', 'relayoutData')
             ])(self.layout_sync(self.figd))
        self.app.callback(
            dash.dependencies.Output('map_france_naissance', 'figure'),
            [dash.dependencies.Input('map_france_deces', 'relayoutData')
             ])(self.layout_sync(self.fign))

        # Department name
        self.app.callback(
            dash.dependencies.Output('list_department_naissance', 'children'),
            [dash.dependencies.Input('map_france_naissance', 'selectedData'),
             ])(self.list_dep_n)
        self.app.callback(
            dash.dependencies.Output('list_department_deces', 'children'),
            [dash.dependencies.Input('map_france_deces', 'selectedData'),
             ])(self.list_dep_d)

    def layout_sync(self, fig_to_sync):
        keys = ['mapbox.center', 'mapbox.zoom', 'mapbox.bearing', 'mapbox.pitch']

        def sync(relayoutData):
            if relayoutData:
                filtered_layout = { k: relayoutData.get(k) for k in keys if k in relayoutData }
                fig_to_sync.update_layout(filtered_layout)
            return fig_to_sync
        
        return sync

    def list_dep_n(self, select):
        dep = self.get_department(select)
        if len(dep) == 96:
            return 'Toute la France'
        else:
            return ','.join([self.dep_map[d] for d in dep])

    def list_dep_d(self, select):
        dep = self.get_department(select)
        if len(dep) == 96:
            return 'Toute la France'
        else:
            return ','.join([self.dep_map[d] for d in dep])

    def fig_naissance(self):
        fign = go.Figure(go.Choroplethmapbox(
            geojson=self.dep,
            name='',
            colorscale='Inferno',
            colorbar=dict(
                title="Naissance",
                tickvals=[np.log10(i) for i in self.tickval],
                ticktext=self.tickval
            ),
            locations=self.depn.index,
            customdata=np.stack((self.depn['NAME'], self.depn.index,
                                 self.depn['SIZE']),
                                axis=1),
            hovertemplate=
            "<b>Departement : %{customdata[1]}</b><br><br>" +
            "Nom : %{customdata[0]}<br>" +
            "Naissance : %{customdata[2]}<br>",
            z=np.log10(self.depn['SIZE']),
            zmin=np.log10(self.zmin),
            zmax=np.log10(self.zmax),
        ))

        fign.update_layout(mapbox_style="carto-positron",
                           mapbox_zoom=4.42,
                           mapbox_center={"lat": 47.0353, "lon": 2.2928},
                           margin={"r": 0, "t": 0, "l": 0, "b": 0},
                           clickmode='event+select',
                           hovermode='closest',
                           )
        return fign

    def fig_deces(self):
        figd = go.Figure(go.Choroplethmapbox(
            geojson=self.dep,
            name='',
            colorscale='Inferno',
            colorbar=dict(
                title="Décès",
                tickvals=[np.log10(i) for i in self.tickval],
                ticktext=self.tickval
            ),
            locations=self.depd.index,
            customdata=np.stack((self.depd['NAME'], self.depd.index,
                                 self.depd['SIZE']),
                                axis=1),
            hovertemplate=
            "<b>Departement : %{customdata[1]}</b><br><br>" +
            "Nom : %{customdata[0]}<br>" +
            "Décès : %{customdata[2]}<br>",
            z=np.log10(self.depd['SIZE']),
            zmin=np.log10(self.zmin),
            zmax=np.log10(self.zmax),
        ))

        figd.update_layout(mapbox_style="carto-positron",
                           mapbox_zoom=4.42,
                           mapbox_center={"lat": 47.0353, "lon": 2.2928},
                           margin={"r": 0, "t": 0, "l": 0, "b": 0},
                           clickmode='event+select',
                           hovermode='closest',
                           )
        return figd

    def get_department(self, hoverData):
        if hoverData is None or hoverData['points'] == []:
            return list(self.dep_map.keys())
        return [p['location'] for p in hoverData['points']]

    def size_france(self, clickDataNaissance, clickDataDeces, nd_val, unmg_val):
        depnid = self.get_department(clickDataNaissance)
        depdid = self.get_department(clickDataDeces)

        what = []
        if unmg_val == 'Unitaire':
            if 'Naissance' in nd_val:
                what += [(d, self.daten, 'SIZE', 'Naissance ' +
                          self.dep_map[d])
                         for d in depnid]

            if 'Décès' in nd_val:
                what += [(d, self.dated, 'SIZE',
                          'Décès ' + self.dep_map[d])
                         for d in depdid]
        else:
            if 'Naissance' in nd_val:
                data = self.daten.loc[depnid].reset_index().groupby(
                    ['date']).sum()
                what += [(None, data, 'SIZE', 'Naissance cumulée')]
            if 'Décès' in nd_val:
                data = self.dated.loc[depdid].reset_index().groupby(
                    ['date']).sum()
                what += [(None, data, 'SIZE', 'Décès cumulé')]

        return self.cts(self.date_axis, what,
                        "Nombre de naissance et décès par mois")

    def size_naissance(self, clickData, unit_mean, type):
        dep = self.get_department(clickData)
        what = []

        if unit_mean == 'Unitaire':
            if 'Femme' in type:
                what += [(d, self.agen, 'SIZEMEREN', 'Femme ' +
                          self.dep_map[d]) for d in dep]
            if 'Homme' in type:
                what += [(d, self.agen, 'SIZEPEREN', 'Homme ' +
                          self.dep_map[d]) for d in dep]
            if 'Somme' in type:
                what += [(d, self.agen, 'SIZEMEREPEREN', 'H/F somme ' +
                          self.dep_map[d]) for d in dep]
            if 'Moyenne' in type:
                what += [(d, self.agen, 'MGMEREPEREN', 'H/F moyenne ' +
                          self.dep_map[d]) for d in dep]

        else:
            data = self.agen.loc[dep].reset_index().groupby(['level_1']).sum()
            if 'Femme' in type:
                what += [(None, data, 'SIZEMEREN', 'Femme cumulée')]
            if 'Homme' in type:
                what += [(None, data, 'SIZEPEREN', 'Homme cumulée')]
            if 'Somme' in type:
                what += [(None, data, 'SIZEMEREPEREN', 'H/F cumulée')]
            if 'Moyenne' in type:
                what += [(None, data, 'MGMEREPEREN', 'H/F moyenne')]

        return self.cts(self.age_naissances_axis, what,
                        "Nombre de naissance en fonction de l'age")

    def size_deces(self, clickData, unit_mean, type):
        dep = self.get_department(clickData)
        what = []

        if unit_mean == 'Unitaire':
            if 'Femme' in type:
                what += [(d, self.aged, 'SIZEMERED', 'Femme ' +
                          self.dep_map[d]) for d in dep]
            if 'Homme' in type:
                what += [(d, self.aged, 'SIZEPERED', 'Homme ' +
                          self.dep_map[d]) for d in dep]
            if 'Somme' in type:
                what += [(d, self.aged, 'SIZEMEREPERED', 'H/F somme ' +
                          self.dep_map[d]) for d in dep]
            if 'Moyenne' in type:
                what += [(d, self.aged, 'MGMEREPERED', 'H/F moyenne ' +
                          self.dep_map[d]) for d in dep]
        else:
            data = self.aged.loc[dep].reset_index().groupby(['AGE']).sum()
            if 'Femme' in type:
                what += [(None, data, 'SIZEMERED', 'Femme cumulée')]
            if 'Homme' in type:
                what += [(None, data, 'SIZEPERED', 'Homme cumulée')]
            if 'Somme' in type:
                what += [(None, data, 'SIZEMEREPERED', 'H/F cumulée')]
            if 'Moyenne' in type:
                what += [(None, data, 'MGMEREPERED', 'H/F moyenne')]

        return self.cts(self.age_deces_axis, what,
                        "Nombre de décès en fonction de l'age")

    def cts(self, x_axis, what, title):
        scatters = []
        for dep, dataframe, w, name in what:
            scatters.append(go.Scatter(
                x=x_axis,
                y=dataframe[w] if dep is None else dataframe.loc[dep][w],
                name=name,
                mode='lines+markers',
            ))

        return {
            'data': scatters,
            'layout': {
                'height': 300,
                'margin': {'l': 50, 'b': 50, 'r': 10, 't': 20},
                'yaxis': {'title': title,
                          'type': 'linear',
                          'font': {'size': 15}},
                'title': {'font': {'size': 15}},
                'legend': {
                    'title': {'font': {'size': 5}},
                    'font': {'size': 11}},
                'xaxis': {'showgrid': False},
                'font': {'size': 10},
            }
        }


if __name__ == '__main__':
    mpj = Naissance()
    mpj.app.run_server(debug=True, port=8051)
