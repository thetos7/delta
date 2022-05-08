                html.Br(),
                html.Div([
                    dcc.Graph(id='insectY',
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
                html.Div(children='coucou', id='label-test'),
                html.Div([
                    dcc.Graph(id='insect_month',
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
                ])


        if application:
            self.app = application

        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
                dash.dependencies.Output('insect_month', 'figure'),
                [dash.dependencies.Input('month_dropdown', 'value'),
                    dash.dependencies.Input('rain_switch', 'on'),
                    dash.dependencies.Input('hour_slider', 'value')]
                )(self.change_month)



        self.app.callback(
            dash.dependencies.Output('insectY', 'figure'),
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

        list_month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

        if id2 + '.n_clicks' == changed_id:
            insect = pd.read_csv('lmsb_animalcrossing/data/insect.csv')
            sel.df = insect
            insectmonth = insect.filter(regex='SH *', axis = 1)
            insect_count = insectmonth.count()

            res = []

            for i in insect_count:
                res.append(i)

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
            }})

        else:
            fish = pd.read_csv('lmsb_animalcrossing/data/fish.csv')
            self.df = fish
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
