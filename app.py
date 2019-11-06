# Dash
from assets import callbacks
from server import app, server
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

# Import assets
import assets.navbar as nb


# This variable is used throughout the application to determine whether the logged in user is admin or not, if they are
# the department variable is used in conjuction to determine which pages get admin access.
isAdmin = False
adminDpt = None
VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password'
}

nav = nb.Navbar()

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])
