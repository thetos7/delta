import dash
from dash import dcc
from dash import html
from Music import Music

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
server = app.server
mus = Music.Song(app)

main_layout = html.Div([
    html.Div(className = "row",
             children=[ 
                 dcc.Location(id='url', refresh=False),
                 html.Div(className="two columns",
                          children = [
                              html.Center(html.H2("Δelta δata")),
                              dcc.Link(html.Button("Score by Genre", style={'width':"100%"}), href='/score&genre'),
                              html.Br(),                              dcc.Link(html.Button("Artists & Popularity", style={'width':"100%"}), href='/artists&popularity'),
                              html.Br(),                              dcc.Link(html.Button("Genre by Country", style={'width':"100%"}), href='/genre&country'),
                              html.Br(),
                              html.Br(),
                              html.Br(),
                              html.Center(html.A('Source Code', href='https://github.com/Stratcher/delta')),
                          ]),
                 html.Div(id='page_content', className="ten columns"),
            ]),
])


home_page = html.Div([
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Markdown("Description des genres de musiques et de leurs popularités"),
])

app.layout = main_layout

app.validation_layout = html.Div([
    main_layout,
    mus.main_layout,
    mus.artists_layout,
    mus.country_layout
])

# Update the index
@app.callback(dash.dependencies.Output('page_content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/score&genre':
        return mus.main_layout
    if pathname == '/artists&popularity':
        return mus.artists_layout
    if pathname == '/genre&country':
        return mus.country_layout
    else:
        return home_page


if __name__ == '__main__':
    app.run_server(debug=True)
