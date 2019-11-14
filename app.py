# Dash
import assets.navbar as nb
import dash_html_components as html
import dash_core_components as dcc
from server import app

# This variable is used throughout the application to determine whether the
# logged in user is admin or not, if they are the department variable is used
# in conjuction to determine which pages get admin access.
isAdmin = False
adminDpt = None

nav = nb.Navbar()

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])
