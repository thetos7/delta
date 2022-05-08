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
        self.levels = ["Niveau dans le diplôme", "Grande discipline", "Secteur disciplinaire"]
        self.years.sort()
        self.cursus_data = self.df.groupby(
            ["Année universitaire", "Type d'établissement", "Grande discipline"]).sum()
        self.cursus_data["Proportion Femmes"] = self.cursus_data["Dont femmes"] / self.cursus_data[
            "Nombre d\'étudiants"]
        self.cursus_data = self.cursus_data.reset_index([1, 2])

        self.main_layout = html.Div([
            html.H4("Treemap de la proportion H/F par type d'établissement et par Grande discipline"),
            dcc.Graph(id="treemap"),
            html.P("Year:"),
            dcc.Slider(id="year", min=0, max=len(self.years) - 1, value=0, step=1,
                       marks=dict(enumerate(self.years))),
            dcc.Markdown(
                '*Utilisez le slider pour voir la répartition H/F parmis les différentes formations au cours des années'
                'années*'),
            dcc.Dropdown(self.levels, self.levels[0], id='level_selection'),
            dcc.Graph(id="scatter")
        ]
        )

        @application.callback(
            Output('scatter', 'figure'),
            Input('level_selection', 'value')
        )
        def update_output(level):
            scatter_data = self.df[["Année universitaire", level, "Nombre d'étudiants", "Dont femmes"]].copy()
            scatter_data["Année universitaire"] = scatter_data[["Année universitaire"]].applymap(
                lambda x: x.split('-')[0]
            )
            scatter_data["Année universitaire"] = pd.to_datetime(scatter_data["Année universitaire"])
            scatter_data = scatter_data.groupby(["Année universitaire", level]).sum()
            scatter_data["Proportion Femmes"] = scatter_data["Dont femmes"] / scatter_data["Nombre d'étudiants"]
            scatter_data = scatter_data.drop(columns=["Nombre d'étudiants", "Dont femmes"]).unstack(level).fillna(0)
            scatter_data = scatter_data["Proportion Femmes"]

            fig = px.scatter(scatter_data, trendline="rolling", trendline_options=dict(window=1),
                             title="Proportion de femmes par regroupement de diplômes",
                             hover_name=level
                             )
            fig.data = [t for t in fig.data if t.mode == "lines"]
            fig.update_traces(showlegend=True)  # trendlines have showlegend=False by default
            return fig

        @application.callback(
            Output("treemap", "figure"),
            Input("year", "value"))
        def display_color(year):
            fig = px.treemap(self.cursus_data.loc[self.years[year]], path=["Type d'établissement", "Grande discipline"],
                             values="Nombre d'étudiants", color="Proportion Femmes", title=self.years[year],
                             range_color=[0.2, 0.9])
            fig.update_layout(autosize=False,
                              width=960,
                              height=960)
            return fig
