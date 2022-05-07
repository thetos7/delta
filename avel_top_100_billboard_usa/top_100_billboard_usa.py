# import dash_design_kit as ddk
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc
from dash import html, Dash, Output, Input, dash_table
import numpy as np
pd.options.plotting.backend = "plotly"


def to_year_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a dataframe with a date column to a dataframe with a year column.
    """
    res = df.copy()
    res["year"] = df["date"].dt.year
    return res


def to_decade(year):
    return year // 10 * 10


def generate_dash_table(dataframe: pd.DataFrame, max_rows: int = 10):
    """
    Generates a dash table from a dataframe.
    :param dataframe: the dataframe to generate the table from
    :param max_rows: the number of rows to display
    :return: html.Table
    """
    return dash_table.DataTable(
        dataframe.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in dataframe.columns],
        page_size=max_rows
    )

class Top100BillboardUSA:
    def __init__(self, application: Dash = None):
        # Importing the data
        self.df = self.load_billboard_dataframe()

        # Creating the Dash application
        self.app = Dash(__name__) if application is None else application
        self.radio_button_options = {
            "Total pour toutes les années": self.get_weeks_on_board_fig(),
            "Total par année": self.get_weeks_on_board_fig_year(),
        }

        # Creating layout and adding callbacks
        self.app.layout = self.main_layout
        self.callbacks()

    @property
    def main_layout(self) -> html.Div:
        """
        Returns the default layout for the Dash application.
        :return: html.Div
        """

        layout = html.Div([
            html.H1('Top 100 Billboard USA'),

            html.H3('Informations à propos des données'),
            html.P(
                f"Il s'agit d'un tableau des classements de la Billboard Hebdomadaire des USA de 1958 à 2021, "
                f"comprenant {len(self.df)} entrées dont {self.song_count} chansons et {self.artist_count} artistes "
                f"uniques. "
            ),
            html.Div([
                html.H3("Distribution du nombre de semaines des musiques au Billboard, de 1958 à 2021"),
                dcc.RadioItems(
                    id="max-weeks-on-board-count-radio",
                    options=list(self.radio_button_options.keys()),
                    value=next(iter(self.radio_button_options.keys())),  # Getting first key of the dict
                    inline=True,
                ),
                html.Div(id='weeks-on-board-count-plots'),
            ]),
            dcc.Markdown('''
            Un large pic est visible à la 20e semaine.   
            Si l'on grossit, on peut également voir la 52e semaine sortir de la tendance.   
            En regardant les mêmes données mais par année,   
            il semblerait que le début des années 90 marque l'arrivée de cette tendance non proportionnelle.   
            Il s'avère qu'à la fin de l'année 1991, le Billboard a institué une "règle de récurrence",   
            stipulant que les chansons qui ont figuré au classement pendant 20 semaines sont retirées si elles se classent en dessous de la 50e place    
            et de même pour les chansons au classement depuis 1 an, si elles se trouvent en dessous de la 25e position.
            '''),

            # dcc.Graph(id="new-artist-on-board", figure=self.get_new_artist_on_board_fig()),

            html.Div([
                html.H3('Entrées fulgurantes'),
                dcc.Graph(id="meteoric-entries-graph", figure=self.get_meteoric_entries_fig()),
                html.P("TODO: add some text"),
            ]),
            html.Div([
                html.H3('Graphs by artist'),
                dcc.Dropdown(id="artist-dropdown", options=self.most_popular_artists, value='Michael Jackson'),
                html.Div(id='artist-dropdown-output'),
            ]),
            html.Div([
                html.H3('À propos'),
                dcc.Markdown('''
                * Source: [Kaggle - Billboard "The hot 100" songs](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs)
                * Copyright © 2022 - Aurélien Visentin - Eliot Leclair
                '''),
            ]),

        ])
        return layout

    def callbacks(self) -> None:
        """
        Adds callbacks to the Dash application.
        :return: None
        """

        # Adding a callback to the artist dropdown
        @self.app.callback(
            Output('artist-dropdown-output', 'children'),
            Input('artist-dropdown', 'value')
        )
        def update_artist_dropdown(artist_name):
            if len(artist_name) == 0:
                return []
            children = [
                dcc.Graph(id=f'music-of-{artist_name}-graph', figure=self.get_music_of_artist_fig(artist_name)),
                # generate_dash_table(self.df[self.df['artist'] == artist_name]),
            ]
            return children

        @self.app.callback(
            Output('weeks-on-board-count-plots', 'children'),
            Input('max-weeks-on-board-count-radio', 'value')
        )
        def update_max_weeks_on_board_count_graphs(input_value):
            # Getting the computed figures from the dict
            return dcc.Graph(id=input_value, figure=self.radio_button_options[input_value])

    @staticmethod
    def load_billboard_dataframe() -> pd.DataFrame:
        df = pd.read_csv('data/top_100_billboard_usa.csv')
        df["date"] = pd.to_datetime(df["date"])
        return df

    def get_music_of_artist_fig(self, artist, df=None, height=1000):
        df = self.df if df is None else df
        df_selected_artist = df[df["artist"] == artist]
        fig = go.Figure()

        fig.update_yaxes(range=[100, 0])
        fig.update_layout(
            title=f"Songs ranking by {artist}",
            xaxis_title="Date",
            yaxis_title="Classement",
            height=height,
            legend={
                "font": {"size": 7},
                "orientation": "h",
                "yanchor": "bottom",
                "xanchor": "center",
                "y": 1.02,
                "x": 1
            }
        )


        for song in df_selected_artist["song"].unique():
            filtered_song_df = df_selected_artist[df_selected_artist["song"] == song].copy()
            tmp = go.Scatter()
            fig.add_scatter(
                x=filtered_song_df["date"],
                y=filtered_song_df["rank"],
                name=song,
                mode='lines+markers',

            )

        return fig

    def get_max_weeks_on_board_count(self, df=None, reindex=True) -> pd.Series:
        """
        Returns the distribution of weeks on board
        :return: pd.Series
        """
        if df is None:
            df = self.df
        max_weeks_on_board_count = df.groupby(by=["artist", "song"])["weeks-on-board"].max().value_counts()
        if reindex:
            max_weeks_on_board_count = max_weeks_on_board_count.reindex(
                list(range(max_weeks_on_board_count.index.min(), max_weeks_on_board_count.index.max() + 1)),
                fill_value=0
            )
        return max_weeks_on_board_count

    def get_weeks_on_board_fig(self, height=600) -> go.Figure:
        """
        Returns a plotly figure of the number of weeks on the billboard.
        :return: plotly.graph_objs.Figure
        """
        # Creating the figure
        max_weeks_on_board_count = self.get_max_weeks_on_board_count()
        fig = max_weeks_on_board_count.plot.bar()

        fig.update_layout(
            xaxis_title="Nombre de semaines",
            yaxis_title="Nombre de musiques",
            height=height,
            showlegend=False
        )

        return fig

    def get_weeks_on_board_fig_year(self, height=600) -> go.Figure:

        tmp_year_list = []
        for year in sorted(self.df.date.dt.year.unique(), reverse=False):
            df_tmp = self.df[self.df["date"].dt.year == year]
            max_weeks_on_board_count = self.get_max_weeks_on_board_count(df_tmp)

            for week, count in max_weeks_on_board_count.items():
                tmp_year_list.append((year, week, count))

        weeks_on_board_year = pd.DataFrame(data=tmp_year_list, columns=["Année", "Semaine", "Compte"])
        weeks_on_board_year = weeks_on_board_year.sort_values(["Année", "Semaine"], ascending=True)

        fig = px.bar(
            weeks_on_board_year,
            x="Semaine",
            y="Compte",
            animation_frame="Année",
            range_x=[0, 52],
            range_y=[0, 250],
            height=height,
        )

        # Setting titles
        fig.update_xaxes(title="Nombre de semaine")
        fig.update_yaxes(title="Nombre de musiques")

        # Setting plot parameters
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 220  # Update animation speed

        return fig

    def get_new_artist_on_board_fig(self) -> go.Figure:
        """
        Returns a plotly figure of the number of weeks on the billboard.
        :return: plotly.graph_objs.Figure
        """

        x, y = [], []
        for year in self.df["date"].dt.year.unique():
            filtered_decade_df = self.df[self.df["date"].dt.year == year]
            artistes_distincts_decade = len(filtered_decade_df["artist"].unique())

            x.append(year), y.append(artistes_distincts_decade)

        # Creating the figure
        return px.line(
            x=x,
            y=y,
            title="Nombre de nouveaux artistes chaque année",
            labels={'x': 'Années', 'y': 'Nombre de nouveaux artistes'}
        )

    def get_meteoric_entries_fig(self, height=600) -> go.Figure:

        new_entry = self.df.loc[np.where((self.df["last-week"]).isna()
                                        & (self.df["rank"] == 1)
                                        & (self.df["date"] != "1958-08-04 00:00:00"))] # en ignorant la toute premiere semaine (100 nouvelles entrées)
        ne_count = new_entry["date"].dt.strftime("%Y").value_counts()
        ne_count = ne_count.reindex(list(["{:4d}".format(x) for x in range(1990, 2022)]), fill_value=0)
        #ne_count = new_entry.value_counts("date").sort_index()
        fig = px.bar(x=ne_count.index.values, y=ne_count.values, height=height)
        fig.update_traces(hovertemplate='%{y} entrées fulgurantes en %{x}')
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Nombre d'entrées fulgurantes")
        return fig

    @property
    def artist_count(self):
        return len(self.df["artist"].unique())

    @property
    def song_count(self):
        return len(self.df["song"].unique())

    @property
    def most_popular_artists(self):
        most_popular_songs = self.df.groupby(by=["artist", "song"], as_index=False)["weeks-on-board"].max()
        # Sorting by people that have the most well ranked songs in the billboard
        return most_popular_songs.groupby("artist")["weeks-on-board"].sum().sort_values(ascending=False).index


if __name__ == '__main__':
    nrg = Top100BillboardUSA()
    nrg.app.run_server(debug=True)
