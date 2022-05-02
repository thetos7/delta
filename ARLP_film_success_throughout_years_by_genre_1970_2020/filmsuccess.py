import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import plotly.express as px
import glob
import pandas as pd
import random
from helper import *
from .data.get_data import extract_data
import numpy as np

#fig = px.scatter(df, x="year", y="gross", size=np.exp(df["total_score"]), size_max=60, hover_name="name", hover_data=["genre"], color=df.genre[df.genre.apply(lambda x: len(x) > 0)].apply(lambda x: x[0]))

class FilmSuccess():

    def __init__(self, application = None):
        df = extract_data()
        
        self.app = dash.Dash(__name__)
    
        colors = { 'Horror' : 'red', 'Mystery' : 'pink', 'Thriller' : 'black',
              'Crime' : 'purple', 'Drama' : 'darkviolet', 'Comedy' : 'indigo',
              'Sci-Fi' : 'blue', 'Music' : 'light blue', 'Action' : 'cyan',
              'Biography' : 'teal', 'History' : 'olive', 'War' : 'light green',
              'Fantasy' : 'lime', 'Romance' : 'yellow', 'Western' : 'moccasin',
              'Family' : 'orange', 'Animation' : 'darkorange',
              'Adventure' : 'brown', 'Musical' : 'grey', 'Sport' : 'darksalmon',}

        fig2_df = pd.DataFrame()
        exploded_df = df.explode("genre")
        genres = exploded_df.genre.unique()
        for genre in genres:
          _df = exploded_df[exploded_df['genre'] == genre]
          _df = _df.groupby('year').mean()
          _df["genre"] = genre
          fig2_df = pd.concat([fig2_df, _df])
        fig2_df = fig2_df.reset_index()

        self.main_layout = html.Div(children = [
                                          html.H3('Films Stats'),
                                          html.Div("Move your mouse over the graph and click onto any of the representation to have additionnal informations. You can click on the gender's legend on the right to mask few ones"),

                                          html.Div(children = [
                                            html.Div([dcc.RadioItems(
                                                id='y_axis',
                                                options=[{'label': i, 'value': i} for i in fig2_df[["profit", "total_score", "votes"]].columns],
                                                value=fig2_df[["profit", "total_score", "votes"]].columns[0],
                                                labelStyle={'display':'block'}
                                              )], style={'display':'flex', 'align-items':'center', 'width':'10%'}),
                                            html.Div([dcc.Graph(id="fig2")], style={'width':'90%'})
                                          ], style={'display':'flex'}),
                                          
                                          html.Div("Move your mouse over bubble for additionnal information about the film. The graph below is selecting the films with the highest and lowest profit to see which films impacted the gender's success or failure during the year"),

                                          html.Div([dcc.Graph(id="fig3")])
                                        ])
                                        
        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        @self.app.callback(
            dash.dependencies.Output('fig2', 'figure'),
            dash.dependencies.Input('y_axis', 'value'))
        def update_fig2(y_value):
          fig = px.line(fig2_df, x="year", y=y_value, color="genre", color_discrete_map=colors, hover_data=["genre"])
          return fig

        @self.app.callback(
            dash.dependencies.Output('fig3', 'figure'),
            dash.dependencies.Input('fig2', 'clickData'))
        def update_fig3(clickData):
          if clickData == None:
            year = random.choice([i for i in range(1970,2021)])
            genre = random.choice(genres.tolist())
          else:
            year = clickData['points'][0]['x']
            genre = clickData['points'][0]['customdata'][0]

          fig3_df = exploded_df[exploded_df.year == year]
          fig3_df = fig3_df[fig3_df.genre == genre]
          fig3_df.drop(fig3_df[fig3_df.profit.isna()].index, inplace=True)
          fig3_df = fig3_df.sort_values(by='profit')
          fig3_df = pd.concat([fig3_df.head(5), fig3_df.tail(5)])

          return px.scatter(fig3_df, x="name", y="profit", title="{} {}".format(year, genre), color="genre", color_discrete_map=colors, size=np.exp(fig3_df.total_score), size_max=60, hover_data={"total_score": True})


    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    filmsuc = FilmSuccess()
    filmsuc.run(port=8055)