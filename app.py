# Dash
from assets import callbacks
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html

# Import assets
import assets.navbar as nb

# This variable is used throughout the application to determine whether the
# logged in user is admin or not, if they are the department variable is used
# in conjuction to determine which pages get admin access.
isAdmin = False
adminDpt = None
VALID_USERNAME_PASSWORD_PAIRS = {
    'username': 'password'
}

app = dash.Dash('Resources and Data Analysis')
app.config.suppress_callback_exceptions = True

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

# Main application loop
if __name__ == '__main__':
    # Uncomment this line to run the actual server
    # app.run_server(debug=False, host='166.20.109.188', port='8080')

    # Uncomment this line to debug locally
    app.run_server(debug=True, host='127.0.0.1', port='8080')
