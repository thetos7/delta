import sys
import dash
from dash.dependencies import Input, Output
import dash_daq as daq
import flask
from dash import dcc
from dash import html
from dash import callback_context
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

def int_to_time(i):
  res = ['All day']
  check_double = 0
  if i >= 4 and i < 21:
    res.append('4 AM – 9 PM')
  if (i > 16 and i < 24) or (i >= 0 and i < 9):
    res.append('4 PM –\xa09 AM')
  if i >= 9 and i < 16:
    res.append('9 AM –\xa04 PM')
    check_double += 1
  if (i >= 21 and i < 24) or (i >= 0 and i < 4):
    res.append('9 PM –\xa04 AM')
    check_double += 1
  if check_double >= 1:
    res.append('9 AM –\xa04 PM; 9 PM – 4 AM')
  return res


def month_to_subset(month):
    if month == 1:
        return 'SH Jan'
    if month == 2:
        return 'SH Feb'
    if month == 3:
        return 'SH Mar'
    if month == 4:
        return 'SH Apr'
    if month == 5:
        return 'SH May'
    if month == 6:
        return 'SH Jun'
    if month == 7:
        return 'SH Jul'
    if month == 8:
        return 'SH Aug'
    if month == 9:
        return 'SH Sep'
    if month == 10:
        return 'SH Oct'
    if month == 11:
        return 'SH Nov'
    if month == 12:
        return 'SH Dec'

class Animal():
    def __init__(self, application = None):
        self.background_color = '#FFFEFF'
        self.title_color = '#540B0E'
        self.trace_color = ['B6F7FF']
        
        self.pie_chart_colors = ['#C4DDFF', '#7FB5FF', '#001D6E', '#FEE2C5']
        self.df = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
        
        self.df['Where/How'] = self.df['Where/How'].map({
                                        'River (clifftop)' : 'River',
                                        'River (mouth)' : 'River',
                                        'River' : 'River',
                                        'Sea' : 'Sea',
                                        'Pond' : 'Pond',
                                        'Pier' : 'Pier',
                                        'Sea (rainy days)' : 'Sea rain'
                                        })
        self.main_layout = html.Div([
            html.Div([
                html.H3(children='Animal Crossing : New Horizons',
                    style={
                        'font-family' : 'FinkHeavy',
                        'font-weight' : 'bold',
                        'font-size' : '30px',
                        'text-align': 'center'
                        }
                    ),
                html.H4('Les collectables du jeu et leur valeur pécunière',
                    style={
                        'font-family' : 'FinkHeavy',
                        'font-size' : '18px',
                        'text-align' : 'center'
                        }
                    )
                ]),
                html.Br(),
                html.Button('Poissons', id='bpoisson',
                    style={
                            'backgroundColor' : '#7FB5FF',
                            'color' : 'white',
                            'border' : '1px black solid',
                            'margin' : '0px 0px 10px 10px'
                        }
                    ),
                html.Button('Insectes', id='binsecte',
                    style={
                            'backgroundColor' : '#CC704B',
                            'color' : 'white',
                            'border' : '1px black solid',
                            'margin' : '0px 0px 10px 10px'
                        }
                    ),
                html.Br(),
                html.Div([
                    dcc.Graph(id='fishY',
                        style={'width' : '75%', 'display':'inline-block'}
                        )
                    ]),
                html.Div([
                    html.Div([dcc.Dropdown(id = 'month_dropdown',
                        options=[
                                {'label' : 'Janvier', 'value' : 1},
                                {'label' : 'Février', 'value' : 2},
                                {'label' : 'Mars', 'value' : 3},
                                {'label' : 'Avril', 'value' : 4},
                                {'label' : 'Mai', 'value' : 5},
                                {'label' : 'Juin', 'value' : 6},
                                {'label' : 'Juillet', 'value' : 7},
                                {'label' : 'Août', 'value' : 8},
                                {'label' : 'Septembre', 'value' : 9},
                                {'label' : 'Octobre', 'value' : 10},
                                {'label' : 'Novembre', 'value' : 11},
                                {'label' : 'Décembre', 'value' : 12}
                        ],
                        value = 1,
                        clearable = False,
                        placeholder="Choisissez un mois de l'année")],
                        style={'width': '220px'}
                    ),
                    html.Div(
                        daq.BooleanSwitch(
                        id = 'rain_switch',
                        on = False,
                        color = '#614124',
                        ),
                        style = {"width" : '200 px',
                                'margin' : '0px 0px 0px 10px ',
                                }
                        )],
                    style={ 'display' : 'flex',
                            'flexDirection' : 'row'}
                ),
                html.Br(),
                html.Div(children='Ici sera mit le clique', id='label-test'),
                html.Div([
                    dcc.Graph(id='fish_month',
                        style={'width' : '100%',
                                'display':'inline-block',
                                }
                    ),
                    dcc.Slider(0, 23, 1,
                                value=12,
                                id='hour_slider'
                    )],
                    style={'width' : '50%'}
                    ),
                ])


        if application:
            self.app = application

        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                dash.dependencies.Output('fish_month', 'figure'),
                [dash.dependencies.Input('month_dropdown', 'value'),
                    dash.dependencies.Input('rain_switch', 'on'),
                    dash.dependencies.Input('hour_slider', 'value')]
                )(self.change_month)



        self.app.callback(
            dash.dependencies.Output('fishY', 'figure'),
            [dash.dependencies.Input('bpoisson', 'n_clicks'),
             dash.dependencies.Input('binsecte', 'n_clicks')],
            [dash.dependencies.State('bpoisson', 'id'),
                dash.dependencies.State('binsecte', 'id')]
            )(self.displayGraph)

        self.app.callback(
            dash.dependencies.Output('label-test', 'children'),
            [dash.dependencies.Input('fish_month', 'clickData')]
                )(self.click_on_data)

    def click_on_data(self, clickData):
        point_info = clickData['points']
        print(point_info[0]['label'])
        return 'eheh'

    
    def displayGraph(self, btn1, btn2, id1, id2):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if id2 + '.n_clicks' == changed_id:
            dfg = pd.read_csv('data/insect.csv')
        else:
            fish = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
            self.df = fish
            fishmonth = fish.filter(regex='SH *', axis = 1)
            fish_count = fishmonth.count()

            res = []

            for i in fish_count:
                res.append(i)

            list_month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
 
            fig = dict({
                "data": [{"type" : "bar",
                            "x" : list_month,
                            "y" : res}],
            "layout": 
            {
                'colorway' : self.trace_color,
                "title": 
                {
                    'font': 
                    {
                        'color' : self.title_color,
                        'size' : '18px',
                        'font-family' : 'FinkHeavy'
                    },
                    "text": "Le nombre de poissons disponibles en fonction du mois"
                },
                'paper_bgcolor': self.background_color,
                'plot_bgcolor': self.background_color
            }})
            return fig



    def change_month(self, month, rain, hour):
        sub = month_to_subset(month)
        tmp = []
        for i in int_to_time(hour):
            tmp.append(self.df[self.df[sub] == i])
        fish_hour = pd.concat(tmp).drop_duplicates()

        res_hour = fish_hour.groupby(['Where/How'])
        sell_mean = res_hour.mean()['Sell']
        if rain:
            res = [int(sell_mean[0]), int(sell_mean[1]), int(sell_mean[2]), int(sell_mean[3]) + int(sell_mean[4])]
        else :
            res = [int(sell_mean[0]), int(sell_mean[1]), int(sell_mean[2]), int(sell_mean[3])]
        x = np.arange(3)
        lieux = ['Jetée', 'Lac', 'Rivière', 'Mer']
        
        fig = go.Figure(data=[go.Pie(labels=lieux, values=res, hole=.2)])
        fig.update_traces(textinfo='value', textfont_size=20,
                marker=dict(colors= self.pie_chart_colors, line=dict(color='#000000', width=2)))
        fig.update_layout(clickmode='event+select')
        return fig

    def run(self, debug=False, port=8050):
        self.app.run_server(host="0.0.0.0", debug=debug, port=port)

if __name__ == '__main__':
    ani = Animal()
    ani.run(port=8055)
