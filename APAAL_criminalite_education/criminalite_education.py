import dash
import json
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from scipy import stats


class Criminalite_Education:
    def __init__(self, application=None):

        education_df = pd.read_csv("APAAL_criminalite_education/data/education.csv")
        attendance_ward = education_df.groupby("ward", as_index=False).mean()

        wards = json.load(open("data/wards.geojson"))

        fig = go.Figure(
            px.choropleth_mapbox(
                attendance_ward,
                geojson=wards,
                locations="ward",
                featureidkey="properties.ward",
                color="suspension",
                color_continuous_scale=["green", "yellow", "red"],
                mapbox_style="carto-positron",
                zoom=9,
                center={
                    "lat": 41.8375,
                    "lon": -87.5440,
                },  # Chicago : 41° 52′ 55″ N, 87° 34′ 40″ O
                opacity=0.5,
                labels={"suspension": "Student average suspension (%)"},
            )
        )

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        self.main_layout = html.Div(
            children=[
                html.H3(
                    children="Analyse de la criminalité et de l'éducation à Chicago"
                ),
                html.Div(
                    [
                        dcc.Graph(id="crim_edu-main-graph", figure=fig),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Br(),
                dcc.Markdown(
                    """
            Illustration géographique de l'assiduité des élèves en fonction de la localisation de leur école par code postal.

            #### À propos

            * Sources : 
            * (c) 2022 Adèle PLUQUET & Adrien ANTON LUDWIG
            """
                ),
            ],
            style={
                "backgroundColor": "white",
                "padding": "10px 50px 10px 50px",
            },
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout


if __name__ == "__main__":
    crim_edu = Criminalite_Education()
    crim_edu.app.run_server(debug=True, port=8051)
