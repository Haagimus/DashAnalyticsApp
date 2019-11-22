# Dash
import assets.navbar as nb
import dash_html_components as html
import dash_core_components as dcc
from server import app

nav = nb.Navbar()

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])
