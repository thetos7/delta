import dash
from dash import dcc
from dash import html
import pandas as pd
import folium


class Olympic:
    def _make_dataframe(self, filename):
        try:
            df = pd.read_csv(self.path + filename)
        except FileNotFoundError:
            self.path = "APTT_sujet/"
            df = pd.read_csv(self.path + filename)
        if filename != 'data/stripped.csv':
            df = df.drop(["City", "Sport", "Gender", "Athlete"], axis=1)
            df = df[df["Year"] >= 1918]
            df.drop(df.index[(df['Country'] == 'YUG') | (df['Country'] == 'TCH') | (df['Country'] == 'AHO') | (
                    df['Country'] == 'EUN') | (df['Country'] == 'IOP') | (df['Country'] == 'IOA')], inplace=True)
        return df

    def __init__(self, application=None):
        self.path = ""
        summer = Olympic._make_dataframe(self, "data/summer.csv")
        winter = Olympic._make_dataframe(self, "data/winter.csv")
        stripped = Olympic._make_dataframe(self, "data/stripped.csv")
        stripped['Event'] = 'Stripped'
        stripped['Discipline'] = 'Stripped'
        self.olympic = pd.concat([summer, winter, stripped])

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de médailles olympiques par pays'),
            html.Iframe(id="map", srcDoc=open(self.path + 'map.html', 'r').read(), width='100%', height='600'),
            html.Div([
                html.Div([html.Div('Medals'),
                          dcc.RadioItems(
                              id='med-spe',
                              options=[{'label': 'Marathon', 'value': 'Marathon'},
                                       {'label': '100M', 'value': '100M'},
                                       {'label': 'Médailles volées', 'value': 'Stripped'}],
                              value='Marathon',
                              labelStyle={'display': 'block'},
                          )
                          ], style={'width': '9em'}),
                html.Div([html.Div('Event'),
                          dcc.Dropdown(
                              id='med-event',
                              options=['Marathon', '100M'],
                              value=1,
                              disabled=False,
                          )]),
                html.Br(),
                dcc.Markdown("""
                Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
                En cliquant ou double-cliquant sur les lignes de la légende, vous choisissez les courbes à afficher.
                
                Notes :
                   * FOD est le fioul domestique.
                   * Pour les prix relatifs, seules les énergies fossiles sont prises en compte par manque de données pour les autres.
                   * Sources : 
                      * [base Pégase](http://developpement-durable.bsocom.fr/Statistiques/) du ministère du développement durable
                      * [tarifs réglementés de l'électricité](https://www.data.gouv.fr/en/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/) sur data.gouv.fr
                """)
            ], style={
                'backgroundColor': 'white',
                'padding': '10px 50px 10px 50px',
            })]
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        self.app.callback(
            dash.dependencies.Output('map', 'srcDoc'),
            [dash.dependencies.Input('med-spe', 'value'),
             dash.dependencies.Input('med-event', 'value')])(self.update_graph)

    def update_graph(self, med_type, name):
        event = self.olympic[self.olympic["Event"] == med_type]
        data = event["Country"].value_counts()
        df = pd.DataFrame.from_dict(data)
        df["ISO"] = list(df.index.values)
        fig = folium.Map(location=[28.5736, 9.0750], tiles=None, zoom_start=2, max_bounds=True, min_zoom=1)
        folium.Rectangle([(-20000, -20000), (20000, 20000)], fill=True, fill_color="#0080ff").add_to(fig)
        url = self.path
        choro = folium.Choropleth(
            geo_data=f'{url}data/countries.geojson',
            name='choropleth',
            data=df,
            columns=['ISO', 'Country'],
            key_on='feature.properties.ISO_A3',
            fill_color='RdPu',
            fill_opacity=1,
            line_opacity=0.8,
            Highlight=True,
            line_color='black',
            nan_fill_color="White",
            legend_name="Number of medals"
        ).add_to(fig)
        for c in choro.geojson.data['features']:
            if c['properties']['ISO_A3'] in df['ISO']:
                c['properties']['Medals'] = float(df.loc[c['properties']['ISO_A3'], 'Country'])
            else:
                c['properties']['Medals'] = 0
        folium.GeoJsonTooltip(['Country', 'Medals']).add_to(choro.geojson)
        folium.LayerControl().add_to(fig)
        fig.save(self.path + "map.html")
        return open(self.path + 'map.html', 'r').read()


if __name__ == '__main__':
    olym = Olympic()
    olym.app.run_server(debug=True, port=8052)
