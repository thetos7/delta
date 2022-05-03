import dash
from dash import html

# TODO create layout
class Accidents:
    def __init__(self, application = None):
        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des accidents de la route en France métropolitaine en 2018')
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

if __name__ == '__main__':
    acc = Accidents()
    acc.app.run_server(debug=True, port=8880)
