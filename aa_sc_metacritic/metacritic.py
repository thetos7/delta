import pandas as pd
import numpy as np
import plotly.express as px 
import dash


def get_data(filename):
    data = pd.read_csv(filename)
    data = data.loc[(data.critics > 5) & (data.genre != "No info")]
    return data

class Metacritic():
    def __init__(self, application=None): 
        # Lien entre note et genre
        data = get_data("../data/vgcritics.csv")
        data['r-date'] = pd.to_datetime(data['r-date'], format='%B %d, %Y')
        data = data.loc[data['user score'] != 'tbd']
        data = data.loc[(data.critics > 5) & (data.genre != "No info")]
        genre_list = ["Action", "Adventure", "Arcade", "Sports", "Fighting", "Open-World", "Role-Playing", "RPG", "Platformer", "Fantasy", "Shooter", "Simulation", "Racing", "Survival"]
        yearTarget = 2002
        data_annual = data.loc[data["r-date"].dt.year == yearTarget]

        def score(row, targetGenre) : 
            if targetGenre in row.genre :
                return row.score
            
        def user_score(row, targetGenre) :
            if targetGenre in row.genre :
                if row[4] != "tbd" : 
                    return float(row[4])

        data_gs = pd.DataFrame()
        for tg in genre_list : 
            meanScore = data_annual.apply(score, targetGenre = tg, axis='columns').mean()
            meanUserScore = data_annual.apply(user_score, targetGenre = tg, axis='columns').mean()
            numberInGenre = data_annual.genre.map(lambda g: tg in g).value_counts().loc[True]
            data_tmp = pd.DataFrame({'genre' : tg, 'Score moyen des critiques' : meanScore, 'Score moyen des utilisateurs': meanUserScore, 'nb_games' : numberInGenre}, index=["A"])
            data_gs = data_gs.append(data_tmp)

        genre_colors = {'Action':'gold', 'Adventure':'green', 'Arcade':'brown', 'Sports':'navy', 'Fighting':'#FF0004', 'Open-World':'#00FF16', 'Role-Playing':'#FFB300', 'RPG':'#FAB900', 'Platformer':'#00FCCD', 'Fantasy':'#FC00AB', 'Shooter':'#A33E02', 'Simulation':'#1F8714', 'Racing':'#9B9B9B', 'Survival':'#825C02'}

        fig = px.scatter(data_gs, x='Score moyen des utilisateurs', y='Score moyen des critiques', color="genre", hover_name="genre",
                        color_discrete_map=genre_colors, title="Score moyen par genre sur Metacritic en " + str(yearTarget),
                        size='nb_games', size_max=50)



        # ------------------

        # Lien entre note et plateforme


        #Need platform / mean score / number of games

        platform_list = ["PC", "XboxOne", "Xbox360", "Xbox", "PlayStation4", "PlayStation3", "PlayStation2", "PlayStation", "Switch", "WiiU", "Wii", "GameCube", "Nintendo64", "Dreamcast", "3DS", "DS", "GameBoyAdvance", "PlayStationVita", "PSP"]
        data_annual = data.loc[data["r-date"].dt.year == yearTarget]

        def score(row, targetPlatform) : 
            if targetPlatform == row.platform :
                return row.score
            
        def user_score(row, targetPlatform) :
            if targetPlatform == row.platform :
                if row[4] != "tbd" : 
                    return float(row[4])

        data_platform = pd.DataFrame()
        previousMeanScore = 0
        for tg in platform_list : 
            meanScore = data_annual.apply(score, targetPlatform = tg, axis='columns').mean()
            if pd.isna(meanScore) : 
                continue
            meanUserScore = data_annual.apply(user_score, targetPlatform = tg, axis='columns').mean()
            numberInPlatform = data_annual.platform.map(lambda g: g == tg).value_counts().loc[True]
            data_tmp = pd.DataFrame({'platform' : tg, 'Score moyen des utilisateurs' : meanScore, 'Score moyen des critiques': meanUserScore, 'nb_games' : numberInPlatform}, index=["A"])
            data_platform = data_platform.append(data_tmp)

        platform_colors = {'PC':'silver',"XboxOne":"greenyellow", "Xbox360":"chartreuse", "Xbox":"lime", "PlayStation4":"navy", "PlayStation3":"blue", "PlayStation2":"dodgerblue", "PlayStation":"cyan", "Switch":"red", "WiiU":"firebrick", "Wii":"lightcoral", "GameCube":"salmon", "Nintendo64":"darkred", "Dreamcast":"sandybrown", "3DS":"#B05500", "DS":"#FF7B00", "GameBoyAdvance":"#F3ED36", "PlayStationVita":"#C9C40E", "PSP":"gold"}

        fig_2 = px.scatter(data_platform, x='Score moyen des utilisateurs', y='Score moyen des critiques', color="platform", hover_name="platform",
                        color_discrete_map=platform_colors, title="Score moyen par plateforme sur Metacritic en " + str(yearTarget),
                        size='nb_games', size_max=50)

        # ----------------------

        data_mean = data.groupby(data['r-date'].dt.year).head(50)
        del data_mean['users']
        del data_mean['critics']

        evolution_per_year = data_mean.groupby(data['r-date'].dt.year).mean()

        fig_evolution_per_year = px.line(evolution_per_year, title="Moyenne des 50 meilleurs jeux par année", labels={
                            "value": "Score moyen",
                            "r-date": "Année",
                        },)

        data_mean = data.groupby(data['r-date'].dt.month).head(50)
        del data_mean['users']
        del data_mean['critics']
        evolution_per_month = data_mean.groupby(data['r-date'].dt.month).mean()

        fig_evolution_per_month = px.line(evolution_per_month, title="Moyenne des 50 meilleurs jeux par mois", labels={
                            "value": "Score moyen",
                            "r-date": "Mois",
                        },)


        from dash import Dash, html, dcc

        app = Dash(__name__)


        app.layout = html.Div(children=[
            html.H1(children='Analyse des notes Metacritic', style={'text-align': 'center', 'font-family': 'Tahoma, sans-serif'}),

            dcc.Markdown("""
                    Metacritic est un agrégateur de note qui prend les notes publiés sur chaque jeux par les plus gros sites parlant de jeu vidéo à travers le monde. Cet outil est aujourd'hui la référence dans le domaine et est souvent utilisé comme étalon pour connaître la qualité d'un jeu. Il est aussi possible pour les utilisateurs de notés les jeux permettant de facilement comparer l'avis des joueurs par rapport à l'avis des critiques.
                    A chaque sortie d'un jeu son score Metacritic est mis en avant sur les réseaux sociaux et est souvent remis en cause par les joueurs estimant que les critiques ont été biaisé soit par du sponsoring soit parce qu'ils deviennent de plus en plus clément avec le temps.
                    ## Objectif
                    Grâce à ces jeux de données nous allons chercher des liens entre les notes Metacritic des critiques et des utilisateurs avec différents parametres comme leur genre, leur plateforme, leur année de sortie et leurs ventes. La visualiation des données par année permet aussi de mettre en avant l'emergence et la "mort" commerciale des consoles et genre.
                    """),

            dcc.Graph(
                id='platform-graph',
                figure=fig_2
            ),

            html.Div([
                        html.Div(
                            dcc.Slider(
                                    id='wps-crossfilter-year-slider',
                                    min=2002,
                                    max=2012,
                                    step = 1,
                                    value=2002,
                                    marks={str(year): str(year) for year in [i for i in range(2002,2012)]},
                            ),
                            style={'display':'inline-block', 'width':"90%"}
                        ),
                        dcc.Interval(            # fire a callback periodically
                            id='wps-auto-stepper',
                            interval=500,       # in milliseconds
                            max_intervals = -1,  # start running
                            n_intervals = 0
                        ),
                        ], style={
                            'padding': '0px 50px', 
                            'width':'100%'
                        }),

            html.Div([
                        html.Div(
                            dcc.Graph(
                                id='evolution-year-graph',
                                figure=fig_evolution_per_year
                            ),    
                            style={'display':'inline-block', 'width':"50%"}
                        ),
                        html.Div(
                            dcc.Graph(
                                id='evolution-month-grapth',
                                figure=fig_evolution_per_month
                            ),    
                            style={'display':'inline-block', 'width':"50%"}
                        ),
                        ], style={
                            'padding': '0px 50px', 
                            'width':'100%'
                        }),
            dcc.Markdown("""## Bilan 
                    Contrairement a la croyance populaire les notes des meilleurs jeux n'augmentent pas d'année en année c'est même l'inverse, on peut observer une descente progressive. 
                                    
                    On peut voir que la période de l'année ayant les meilleurs jeux est en novembre. C'est à ce moment là que sorte beaucoup de très grosses production pour profiter des ventes de noël. A l'inverse l'été est une période creuse où sorte en moyenne moins de très bons jeux. 
                    """)
            
        ])
        
        self.app.callback(
            dash.dependencies.Output('platform-graph', 'figure'),
            [dash.dependencies.Input('wps-crossfilter-year-slider', 'value')])(update_graph)

    def update_graph2(year):
            yearTarget = year
            platform_list = ["PC", "XboxOne", "Xbox360", "Xbox", "PlayStation4", "PlayStation3", "PlayStation2", "PlayStation", "Switch", "WiiU", "Wii", "GameCube", "Nintendo64", "Dreamcast", "3DS", "DS", "GameBoyAdvance", "PlayStationVita", "PSP"]
            data_annual = data.loc[data["r-date"].dt.year == yearTarget]

            def score(row, targetPlatform) : 
                if targetPlatform == row.platform :
                    return row.score
                
            def user_score(row, targetPlatform) :
                if targetPlatform == row.platform :
                    if row[4] != "tbd" : 
                        return float(row[4])

            data_platform = pd.DataFrame()
            previousMeanScore = 0
            for tg in platform_list : 
                meanScore = data_annual.apply(score, targetPlatform = tg, axis='columns').mean()
                if pd.isna(meanScore) : 
                    continue
                meanUserScore = data_annual.apply(user_score, targetPlatform = tg, axis='columns').mean()
                numberInPlatform = data_annual.platform.map(lambda g: g == tg).value_counts().loc[True]
                data_tmp = pd.DataFrame({'platform' : tg, 'Score moyen des utilisateurs' : meanScore, 'Score moyen des critiques': meanUserScore, 'nb_games' : numberInPlatform}, index=["A"])
                data_platform = data_platform.append(data_tmp)

            platform_colors = {'PC':'silver',"XboxOne":"greenyellow", "Xbox360":"chartreuse", "Xbox":"lime", "PlayStation4":"navy", "PlayStation3":"blue", "PlayStation2":"dodgerblue", "PlayStation":"cyan", "Switch":"red", "WiiU":"firebrick", "Wii":"lightcoral", "GameCube":"salmon", "Nintendo64":"darkred", "Dreamcast":"sandybrown", "3DS":"#B05500", "DS":"#FF7B00", "GameBoyAdvance":"#F3ED36", "PlayStationVita":"#C9C40E", "PSP":"gold"}

            fig_2 = px.scatter(data_platform, x='Score moyen des utilisateurs', y='Score moyen des critiques', color="platform", hover_name="platform",
                            color_discrete_map=platform_colors, title="Score moyen par plateforme sur Metacritic en " + str(yearTarget),
                            size='nb_games', size_max=50)
            return fig_2

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)