from dash import html
from dash import dcc

class Polution():
    def __init__(self, application = None):

        self.main_layout = html.Div(children=[
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("dans l'index à gauche."),
            ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout





if __name__ == '__main__':
    nrg = Energies()
    nrg.app.run_server(debug=True, port=8051)
