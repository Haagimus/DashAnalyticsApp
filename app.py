# Dash
import assets.navbar as nb
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from server import app
import assets.callbacks

nav = nb.navbar()

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    dbc.Col(
        html.Div(id='page-content')
    ),
])
