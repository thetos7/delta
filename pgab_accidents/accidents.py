from typing import Union
import dash
from dash import html
import dash_core_components as dcc
import os

# TODO create layout
class Accidents:
    def __init__(self, application = None):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        map_html: Union[str, None] = None
        try:
            with open(f'{file_dir}/map.html', 'r') as map_file:
                map_html = map_file.read()
        except FileNotFoundError: # Allow missing map file, for now
            pass

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des accidents de la route en France métropolitaine en 2018'),
            html.Iframe(
                srcDoc=map_html,
                style={
                    'min-height': '80vh'
                }
            ) if map_html is not None else dcc.Markdown("""
            Map HTML file is missing.  
            It may not have generated correctly.
            """),
        ], style={
            'backgroundColor': 'white',
            'padding': '10px 50px 10px 50px',
            'display': 'flex',
            'flex-direction': 'column'
        })

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

if __name__ == '__main__':
    acc = Accidents()
    acc.app.run_server(debug=True, port=8880)
