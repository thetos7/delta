#!/usr/bin/env python3

from typing import Tuple

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from .get_data import get_train_data, get_cities, Coords


class TBGT:
    FRANCE_CENTER = (46.7110, 1.7191)
    RELATION_DEFAULT = "TOUTES LES LIGNES"

    def _get_relations_radio(self) -> dcc.RadioItems:
        relations = [self.RELATION_DEFAULT] + list(self.train_df.groups.keys())
        return html.Div([
            "Grandes lignes SNCF:",
            dcc.RadioItems(
                relations,
                value=self.RELATION_DEFAULT,
                id="relations",
                style={"font-size": "10px", "margin": "10px"}
            )
        ], style={"display": "inline-block", "width": "20%"})

    def _get_coords(self, src: str, dst: str) -> Tuple[Coords, Coords]:
        return (
            (self.cities[src][0], self.cities[dst][0]),
            (self.cities[src][1], self.cities[dst][1])
        )

    def _get_map(self, relation: str = RELATION_DEFAULT) -> go.Figure:
        lat_coords, lon_coords = [], []
        cities_name = []
        if (relation != self.RELATION_DEFAULT):
            cities_name = relation.split(" - ")
            lat_coords, lon_coords = self._get_coords(*cities_name)

        with open("TBGT_population_vs_train_speed/.mapbox_token") as f:
            mapbox_access_token = f.read()

        fig = go.Figure(go.Scattermapbox(
            lat=[*lat_coords],
            lon=[*lon_coords],
            mode="markers+lines",
            marker=go.scattermapbox.Marker(size=14),
            text=[*cities_name],
        ))

        fig.update_layout(
            title=f"Ligne: {relation}",
            hovermode="closest",
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=self.FRANCE_CENTER[0],
                    lon=self.FRANCE_CENTER[1]
                ),
                pitch=0,
                zoom=3.5
            )
        )

        return fig

    def __init__(self, application = None):
        self.train_df = get_train_data()
        self.cities = get_cities()

        self.main_layout = html.Div(children=[
            html.H3(
                "Évolution de la population des villes françaises "
                "vis-à-vis du développement des grandes lignes SNCF"
            ),
            html.Div([
                self._get_relations_radio(),
                dcc.Graph(id="map", figure=self._get_map(),
                          style={"display": "inline-block", "width": "75%",
                                 "position": "relative", "vertical-align": "top"}),
            ])
        ], style={
            "backgroundColor": "white",
            "padding": "10px 50px 10px 50px",
        })

        if (application is not None):
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


        ### CALLBACKS ###
        self.app.callback(
            Output("map", "figure"),
            Input("relations", "value")
        )(self._get_map)
