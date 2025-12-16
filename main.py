import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from src.pages import home
from config import CONFIG

# Initialisation de l'app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout global
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Navigation simple (multi-page)
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return home.layout
    return html.H1("404 - Page non trouvée")

home.register_callbacks(app)
# Lancement
if __name__ == '__main__':
    app.run(
        host=CONFIG['APP_HOST'],
        port=CONFIG['APP_PORT'],
        debug=CONFIG['DEBUG']
    )
