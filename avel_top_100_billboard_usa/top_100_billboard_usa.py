# import dash_design_kit as ddk
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc
from dash import html, Dash, Output, Input, dash_table

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
        self.app.layout = self.main_layout

        # Adding callbacks
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
            dcc.Markdown(f'''
            
            Il s'agit d'un tableau des classements de la Billboard Hebdomadaire des USA de 1958 à 2021,   
            comprenant {len(self.df)} entrées dont {self.song_count} chansons et {self.artist_count} artistes uniques.
            
            
            '''),
            dcc.Graph(id='weeks-on-board-plot', figure=self.get_weeks_on_board_fig()),
            dcc.Markdown('''
            Un large pic est visible à la 20e semaine.   
            En grossissant on voit également la 52e semaine sortant de la tendance.   
            Regardons ce même graphique par année. => lien autre page ? [test](/recurrent_rule)   
            Il semblerait que le début des années 90 marque l'arrivée de cette tendance non proportionelle.   
            Il s'avère qu'à la fin de l'année 1991, le Billboard a institué une "règle de récurrence",   
            stipulant que les chansons qui ont figuré au classement pendant 20 semaines sont retirées si elles se classent en dessous de la 50e place.   
            De même pour les chansons au classement depuis 1 an, si elles se trouvent en dessous de la 25e position.   
            '''),
            dcc.Graph(id='weeks-on-board-fig-year', figure=self.get_weeks_on_board_fig_year()),
            dcc.Graph(id='new_artist_on_board_fig', figure=self.get_new_artist_on_board_fig()),

            html.H3('Graphs by artist'),
            dcc.Dropdown(id="artist-dropdown", options=self.df.artist.unique().tolist(), value='Michael Jackson'),
            html.Div(id='artist-dropdown-output'),
            # html.Div([
            #     "Input: ",
            #     dcc.Input(id='my-input', value='', type='text')
            # ]),
            # html.Table(id='foo'),

            html.H3('Notes'),
            dcc.Markdown('''
            ### Sources   
            https://www.billboard.com/billboard-charts-legend/
            '''),

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
        def update_artist_dropdown(input_value):
            return generate_dash_table(self.df[self.df['artist'] == input_value])

    @staticmethod
    def load_billboard_dataframe() -> pd.DataFrame:
        df = pd.read_csv('data/top_100_billboard_usa.csv')
        df["date"] = pd.to_datetime(df["date"])
        return df

    def get_max_weeks_on_board_count(self, df=None) -> pd.Series:
        """
        Returns the distribution of weeks on board
        :return: pd.Series
        """
        if df is None:
            df = self.df
        max_weeks_on_board_count = df.groupby(by=["artist", "song"])["weeks-on-board"].max().value_counts()
        return max_weeks_on_board_count

    def get_weeks_on_board_fig(self):
        """
        Returns a plotly figure of the number of weeks on the billboard.
        :return: plotly.graph_objs.Figure
        """
        # Creating the figure
        max_weeks_on_board_count = self.get_max_weeks_on_board_count()
        fig = max_weeks_on_board_count.reindex(
            list(range(1, max_weeks_on_board_count.index.max() + 1)),
            fill_value=0
        ).plot.bar()

        fig.update_layout(showlegend=False)

        fig.update_layout(title="Distribution du nombre de semaines des musiques au Billboard, de 1958 à 2021")
        fig.update_layout(xaxis_title="Nombre de semaines", yaxis_title="Nombre de musiques")
        return fig

    def get_weeks_on_board_fig_year(self):

        tmp_year_list = []
        for year in sorted(self.df.date.dt.year.unique(), reverse=False):
            df_tmp = self.df[self.df["date"].dt.year == year]

            max_weeks_on_board_count = self.get_max_weeks_on_board_count(df_tmp)

            max_weeks_on_board_count = max_weeks_on_board_count.reindex(
                range(1, max_weeks_on_board_count.index.max() + 1), fill_value=0)
            for week, count in max_weeks_on_board_count.items():
                tmp_year_list.append((year, week, count))

        weeks_on_board_year = pd.DataFrame(data=tmp_year_list, columns=["year", "week", "count"])
        weeks_on_board_year = weeks_on_board_year.sort_values(["year", "week"], ascending=True)
        fig = px.bar(weeks_on_board_year, x="week", y="count", animation_frame="year")

        # Setting titles
        fig.update_layout(xaxis_title="Nombre de semaines", yaxis_title="Nombre de musiques")
        fig.layout.sliders[0].currentvalue = {'prefix': 'Année: '} # Update slider label

        # Setting plot parameters
        fig.update_xaxes(range=[0, 52]), fig.update_yaxes(range=[0, 250])  # Set the range of all axis
        fig.update_layout(height=800)
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 250  # Update animation speed

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
        return px.line(title="Nombre de nouvels artistes chaque année", x=x, y=y,
                       labels={'x': 'Années', 'y': 'Nombre de nouvels artistes'})

    @property
    def artist_count(self):
        return len(self.df["artist"].unique())

    @property
    def song_count(self):
        return len(self.df["song"].unique())


if __name__ == '__main__':
    nrg = Top100BillboardUSA()
    nrg.app.run_server(debug=True)
