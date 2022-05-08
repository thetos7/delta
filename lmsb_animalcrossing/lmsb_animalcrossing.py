import sys
import dash
from dash.dependencies import Input, Output
import dash_daq as daq
import flask
import matplotlib.pyplot as plt
from dash import dcc
from dash import dash_table
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


def month_to_subset(month, north):
    if month == 1:
        if north:
            return 'NH Jan'
        return 'SH Jan'
    if month == 2:
        if north:
            return 'NH Feb'
        return 'SH Feb'
    if month == 3:
        if north:
            return 'NH Mar'
        return 'SH Mar'
    if month == 4:
        if north:
            return 'NH Apr'
        return 'SH Apr'
    if month == 5:
        if north:
            return 'NH May'
        return 'SH May'
    if month == 6:
        if north:
            return 'NH Jun'
        return 'SH Jun'
    if month == 7:
        if north:
            return 'NH Jul'
        return 'SH Jul'
    if month == 8:
        if north:
            return 'NH Aug'
        return 'SH Aug'
    if month == 9:
        if north:
            return 'NH Sep'
        return 'SH Sep'
    if month == 10:
        if north:
            return 'NH Oct'
        return 'SH Oct'
    if month == 11:
        if north:
            return 'NH Nov'
        return 'SH Nov'
    if month == 12:
        if north:
            return 'NH Dec'
        return 'SH Dec'

def convert_where(place):
    if place == 'Jetée':
        return 'Pier'
    if place == 'Mer':
        return 'Sea'
    if place == 'Lac':
        return 'Pond'
    if place == 'Rivière':
        return 'River'

class Animal():
    def __init__(self, application = None):
        self.background_color = '#FFFEFF'
        self.title_color = '#540B0E'
        self.trace_color = ['B6F7FF']

        self.north = True
        self.onglet = 'POISSON'
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
                daq.BooleanSwitch(
                    id = 'north_switch',
                    label = 'Hemisphère Nord',
                    on = True
                )
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
                        label = 'Pluie',
                        color = '#614124'
                        ),
                        style = {"width" : '200 px',
                                'margin' : '0px 0px 0px 10px ',
                                }
                        )
                    ],
                    style={ 'display' : 'flex',
                            'flexDirection' : 'row'}
                ),
                html.Br(),
                html.P(id='trash'),
                html.Div([
                    html.Div([
                    dcc.Graph(id='fish_month',
                        style={'width' : '100%',
                                'display':'inline-block',
                                }
                    ),
                    dcc.Slider(0, 23, 1,
                                value=12,
                                marks={
                                    0: '00h',
                                    1: '01h',
                                    2: '02h',
                                    3: '03h',
                                    4: '04h',
                                    5: '05h',
                                    6: '06h',
                                    7: '07h',
                                    8: '08h',
                                    9: '09h',
                                    10: '10h',
                                    11: '11h',
                                    12: '12h',
                                    13: '13h',
                                    14: '14h',
                                    15: '15h',
                                    16: '16h',
                                    17: '17h',
                                    18: '18h',
                                    19: '19h',
                                    20: '20h',
                                    21: '21h',
                                    22: '22h',
                                    23: '23h',
                                },
                                id='hour_slider'
                    )],
                    style={'width' : '50%'}
                    ),
                    html.Div([
                        dash_table.DataTable(id='tableau_poisson')], 
                    style={'width'
                        :'50%'}
                    )
                ],
                style={ 'display' : 'flex',
                            'flexDirection' : 'row'}
                )
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
                    dash.dependencies.Input('bpoisson', 'n_clicks'),
                    dash.dependencies.Input('binsecte', 'n_clicks'),
                    dash.dependencies.Input('hour_slider', 'value'),
                    dash.dependencies.Input('north_switch', 'on')]
                )(self.change_month)



        self.app.callback(
            dash.dependencies.Output('fishY', 'figure'),
            [dash.dependencies.Input('bpoisson', 'n_clicks'),
             dash.dependencies.Input('binsecte', 'n_clicks'),
             dash.dependencies.Input('north_switch', 'on')],
            [dash.dependencies.State('bpoisson', 'id'),
                dash.dependencies.State('binsecte', 'id')]
            )(self.displayGraph)

        self.app.callback(
            dash.dependencies.Output('tableau_poisson', 'data'),
            [dash.dependencies.Input('fish_month', 'clickData'),
            dash.dependencies.Input('month_dropdown', 'value'),
            dash.dependencies.Input('hour_slider', 'value'),
            dash.dependencies.Input('rain_switch', 'on')]
                )(self.click_on_data)

    def click_on_data(self, clickData, month, hour, rain):
        point_info = clickData['points']
        fish = self.df
        sub = month_to_subset(month)
        lieu = convert_where(point_info[0]['label'])
        if rain :
            fish = fish[fish['Where/How'].str.match(lieu)]
        else:
            fish = fish[fish['Where/How'] == lieu]
        fish = fish[fish[sub].notnull()]
        res = []
        for i in int_to_time(hour):
            res.append(fish[fish[sub] == i])
        fish_hour = pd.concat(res).drop_duplicates()
        for i in fish_hour.columns:
            if i != 'Sell' and i != 'Name' and i != 'Catch Difficulty':
                fish_hour = fish_hour.drop(columns=i)
        fish_hour = fish_hour.sort_values(by=['Sell'], ascending=False)
        return fish_hour.to_dict('records')


    def displayGraph(self, btn1, btn2,north, id1, id2):
        print(north)
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        list_month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        if id2 + '.n_clicks' == changed_id:
            self.onglet = 'INSECTE'
        if id1 + '.n_clicks' == changed_id:
            self.onglet = 'POISSON'
        if self.onglet == 'INSECTE':
            insect = pd.read_csv('lmsb_animalcrossing/data/insects.csv')
            self.df = insect
            if north:
                insectmonth = insect.filter(regex='NH *', axis = 1)
            else:
                insectmonth = insect.filter(regex='SH *', axis = 1)
            insect_count = insectmonth.count()
            res = []
            for i in insect_count:
                res.append(i)
            print(len(res))
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
                        "text": "Le nombre d'insectes disponibles en fonction du mois"
                    },
                    'paper_bgcolor': self.background_color,
                    'plot_bgcolor': self.background_color
                }
            })
        else:
            self.onglet = 'POISSON'
            fish = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
            self.df = fish
            if north:
                fishmonth = fish.filter(regex='NH *', axis = 1)
            else:
                fishmonth = fish.filter(regex='SH *', axis = 1)
            fish_count = fishmonth.count()
            res = []
            for i in fish_count:
                res.append(i)
            fig = dict({
                "data": [{"type" : "bar",
                            "x" : list_month,
                            "y" : res}],
                "layout": 
                {
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
                }
            })
        return fig



    def change_month(self, month, rain, btn1, btn2, hour, north):
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        sub = month_to_subset(month, north)
        tmp = []
        for i in int_to_time(hour):
            tmp.append(self.df[self.df[sub] == i])
        fish_hour = pd.concat(tmp).drop_duplicates()

        res_hour = fish_hour.groupby(['Where/How'])
        sell_mean = res_hour.mean()['Sell']
        changed_id = [p['prop_id'] for p in callback_context.triggered][0]
        if self.onglet == 'POISSON':
            if rain:
                res = [int(sell_mean[0]), int(sell_mean[1]), int(sell_mean[2]), int(sell_mean[3]) + int(sell_mean[4])]
            else :
                res = [int(sell_mean[0]), int(sell_mean[1]), int(sell_mean[2]), int(sell_mean[3])]
            x = np.arange(3)
            lieux = ['Jetée', 'Lac', 'Rivière', 'Mer']
        else:
            res = []
            for i in sell_mean:
                res.append(int(i))
            x = np.arange(24)
            lieux = ['Caché sur le rivage', 'Caché sous les arbres', 'Volant', 'Volant près des fleurs bleues, violettes ou noires', 'Volant près des fleurs', 'Volant près de déchets ou de navets pourris', 'Volant près des sources de lumière', "Volant près de l'eau", "En tapant des pierres", "Sur des rochers", "Sur des fleurs", "Sur des bois feuillus ou des cèdres", "Sur des palmiers", "Sur des rivières ou des lacs", "Sur des pierres ou des buissons", "Sur des navets pourris", "Sur le sol", "Sur des souches", "Sur des arbres", "Sur des villageois", "Sur des fleurs blanches", "En train de pousser des boules de neige", "En secouant des arbres (cèdres ou feuillus", "Sous un sol en creusant"]
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
