import pandas as pd  # DataFrame
from dash import dcc, html, Input, Output, dash  # App
import plotly.express as px
import os  # Path management


class Formations:

    def __init__(self, application=None):

        self.main_layout = None
        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        self.df = pd.read_csv(os.getcwd() + "/formations/data/formations.csv", low_memory=False)

        self.years = self.df["Année universitaire"].unique().tolist()
        self.years.sort()
        cursus_data = self.df.groupby(
            ["Année universitaire", "Type d'établissement", "Grande discipline"]).sum()
        cursus_data["Proportions Femmes"] = cursus_data["Dont femmes"] / cursus_data["Nombre d\'étudiants"]
        cursus_data = cursus_data.reset_index([1, 2])

        self.main_layout = html.Div([
            html.H4('Treemap of female proportion in formations'),
            dcc.Graph(id="graph"),
            html.P("Year:"),
            dcc.Slider(id="year", min=0, max=len(self.years) - 1, value=0, step=1,
                       marks=dict(enumerate(self.years)))
        ])

        @application.callback(
            Output("graph", "figure"),
            Input("year", "value"))
        def display_color(year):
            fig = px.treemap(cursus_data.loc[self.years[year]], path=["Type d'établissement", "Grande discipline"],
                             values="Nombre d'étudiants", color="Proportions Femmes", title=self.years[year],
                             range_color=[0.2, 0.9])
            fig.update_layout(autosize=False,
                              width=960,
                              height=960)
            return fig
