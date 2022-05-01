# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import numpy as np
import math
from pandas.core.frame import DataFrame
import plotly.express as px
import pandas as pd


def to_int_list(to_convert):
    try:
        return list(map(int, to_convert))
    except ValueError:
        return [math.inf]


def compute_x(df, x_axis):
    if x_axis[-3:] == "Elo":
        x_selector = pd.cut(df[x_axis], np.arange(0, 3000, 100))
        x_mapper = lambda interval: int(round(interval.mid))
        plot_method = "scatter"
        grp_by_x = df.groupby(x_selector)
        return grp_by_x, x_selector, x_mapper, plot_method

    if x_axis == "TimeControl":
        x_mapper, plot_method = lambda x: x, "bar"
        df = df.sort_values(
            "TimeControl",
            key=lambda serie: [to_int_list(format) for format in serie.str.split("+")],
        )
        grp_by_x = df.groupby(x_axis, sort=False)
        return grp_by_x, x_axis, x_mapper, plot_method

    raise ValueError(x_axis, "is an unknown x axis selector")


def compute_y(grp_by_x, y_axis):
    if y_axis[-7:] == "Winrate":
        color = y_axis[:-7]
        color_win = "1-0" if color == "White" else "0-1"
        color_wins = grp_by_x["Result"].apply(lambda x: x[x == color_win].count())
        other_wins = grp_by_x["Result"].apply(lambda x: x[x == color_win[::-1]].count())
        winrate = (color_wins / (color_wins + other_wins)).rename(y_axis)
        winrate = winrate.round(2).reset_index()
        y_range = [0, 1]
        return winrate, y_range

    if y_axis == "TimeTermination":
        time_forfeits = grp_by_x["Termination"].apply(
            lambda x: x[x == "Time forfeit"].count()
        )
        total_termination = grp_by_x["Termination"].count()
        timerate = (time_forfeits / total_termination).rename(y_axis)
        timerate = timerate.round(2).reset_index()
        y_range = [0, 1]
        return timerate, y_range

    raise ValueError(y_axis, "is an unknown y axis selector")


def compute_plot(df, x_axis, x_labels, y_axis, y_labels, x_max_size=30):
    methods_dict = {"scatter": px.scatter, "bar": px.bar}
    grp_by_x, x_selector, x_mapper, plot_method = compute_x(df, x_axis)

    if grp_by_x.ngroups > x_max_size and plot_method != "scatter":
        last_most_used = grp_by_x.size().sort_values(ascending=False).iloc[x_max_size]
        last_most_used = 1 if last_most_used <= 0 else last_most_used
        grp_by_x = grp_by_x.filter(
            lambda grp: grp[x_axis].count() >= last_most_used
        ).groupby(x_selector, sort=False)

    plot_data, y_range = compute_y(grp_by_x, y_axis)
    plot_data[x_axis] = plot_data[x_axis].apply(x_mapper)
    figure = methods_dict[plot_method](
        plot_data,
        x=x_axis,
        y=y_axis,
        labels={x_axis: x_labels[x_axis], y_axis: y_labels[y_axis]},
    )
    figure.update_yaxes(range=y_range)
    return figure


def main():
    df = pd.read_csv(
        "../../data/lichess_db_standard_rated_2013-01.csv",
        dtype={
            "Event": "string",
            "Site": "string",
            "White": "string",
            "Black": "string",
            "Result": "string",
            "UTCDate": "string",
            "UTCTime": "string",
            "WhiteElo": "float64",
            "BlackElo": "float64",
            "WhiteRatingDiff": "float64",
            "BlackRatingDiff": "float64",
            "ECO": "string",
            "Opening": "string",
            "TimeControl": "string",
            "Termination": "string",
            "BlackTitle": "string",
            "WhiteTitle": "string",
            "Moves": "string",
        },
    )
    df = DataFrame(df)

    x_labels = {
        "WhiteElo": "Classement des blancs",
        "BlackElo": "Classement des noirs",
        "TimeControl": "Mode de jeu",
    }
    y_labels = {
        "WhiteWinrate": "Pourcentage de victoire des blancs",
        "BlackWinrate": "Pourcentage de victoire des noirs",
        "TimeTermination": "Pourcentage de partie finies au temps",
    }

    app = Dash(__name__)

    x_drop_opts = {value: key for key, value in x_labels.items()}
    y_drop_opts = {value: key for key, value in y_labels.items()}
    app.layout = html.Div(
        [
            html.Label(
                ["X axis:"], style={"font-weight": "bold", "text-align": "center"}
            ),
            dcc.Dropdown(options=x_labels, value="WhiteElo", id="x_drop_down"),
            html.Label(
                ["Y axis:"], style={"font-weight": "bold", "text-align": "center"}
            ),
            dcc.Dropdown(options=y_labels, value="WhiteWinrate", id="y_drop_down"),
            dcc.Graph(id="graph"),
        ]
    )

    @app.callback(
        Output("graph", "figure"),
        inputs=[Input("x_drop_down", "value"), Input("y_drop_down", "value")],
    )
    def update_graph(x_axis, y_axis):
        return compute_plot(df, x_axis, x_labels, y_axis, y_labels)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
