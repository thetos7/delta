import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px

class Polution():
    def get_pollution_per_vehicules_in_france(self):
        df = pd.read_csv("data/vehicules_polluant_france_2015.csv",sep=";",encoding="latin1")

        columns_to_keep = ['lib_mrq_doss', 'hc', 'nox', 'hcnox', 'ptcl', 'co2_mixte', 'co_typ_1','hybride','energ']
        df = df[columns_to_keep]
        df.columns = ['Marque', 'Emission HC', 'Emission NOx', 'Emission HC et NOx', 'Emission de Particules', 'Emission CO2', 'Emission CO type1', 'Hybride', 'Carburant']
        df = transform_energ_names(df, "Carburant")
        df["Hybride"].replace({"non ": False,"oui ": True}, inplace = True)
        return df

    def __init__(self, application = None):
        self.df = self.get_pollution_per_vehicules_in_france()
        self.main_layout = html.Div(children=[
    html.H3(children='Évolution des prix de différentes énergies en France'),
    html.Div([ dcc.Graph(id='pol-main-graph'), ], style={'width':'100%', }),
    html.Div([
            html.Div([ html.Div('Prix'),
                dcc.RadioItems(
                id='pol-price-type',
                options=[{'label':'Absolu', 'value':"NOx"}, 
                        {'label':'Équivalent J','value':"HC et NOx"},
                        {'label':'Relatif : 1 en ','value':"HC"}],
                        value="NOx",
                        labelStyle={'display':'block'},
                )
            ])])], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
        self.app.callback(
                    dash.dependencies.Output('pol-main-graph', 'figure'),
                    [ dash.dependencies.Input('pol-price-type', 'value'),
                    ])(self.update_graph)

    def update_graph(self, name="HC et Nox"):
        col = f"Emission {name}"
        agg = (
            self.df.copy()[["Marque", col]]
            .groupby(["Marque"])
            .mean()
            .reset_index()
            .sort_values(by=[col, "Marque"])
            # .replace(np.NaN,0)
        )

        fig = px.bar(agg, y=col, x="Marque", title=f"Moyenne d'{col} pour les modèles par marque")
        fig.update_traces(
            textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
        )
        return fig


def transform_energ_names(df,col):
    energ_name = {'ES ': 'Essence',
                  'GO ': 'Gazole',
                  'ES/GP ': 'Essence ou Gaz de Pétrole Liquéfié',
                  'GP/ES ': 'Essence ou Gaz de Pétrole Liquéfié',
                  'EE ': 'Essence Hybride rechargeable',
                  'EL ': 'Electricité',
                  'EH ': 'Essence Hybride non rechargeable',
                  'GH ': 'Gazole Hybride non rechargeable',
                  'ES/GN ': 'Essence ou Gaz Naturel',
                  'GN/ES ': 'Essence ou Gaz Naturel',
                  'FE ': 'Superéthanol',
                  'GN ': 'Gaz Naturel',
                  'GL ': 'Gazole Hybride rechargeable'}
    df[col].replace(energ_name, inplace = True)
    return df


if __name__ == '__main__':
    pol = Energies()
    pol.app.run_server(debug=True, port=8051)
