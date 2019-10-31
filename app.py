# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input  # Used for callbacks

# Import assets
import assets.navbar as nb

# Import pages
from pages.home import Home
from pages.programs import Programs
from pages.employees import EmployeeTable

# This variable is used throughout the application to determine whether the logged in user is admin or not, if they are
# the department variable is used in conjuction to determine which pages get admin access.
isAdmin = False
adminDpt = None

nav = nb.Navbar()

app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content')
])

# These callbacks handle main page functionality like content loading
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return EmployeeTable()
    if pathname == '/programs':
        return Programs()
    if pathname == '/':
        return Home()

# These callbacks just set the active class for the navbar so it colors properly
@app.callback(Output('homeLink', 'className'), [Input('url', 'pathname')])
def HomeLink(pathname):
    if pathname == '/':
        return 'active'


@app.callback(Output('empLink', 'className'), [Input('url', 'pathname')])
def EmpLink(pathname):
    if pathname == '/employees':
        return 'active'


@app.callback(Output('pgmLink', 'className'), [Input('url', 'pathname')])
def PgmLink(pathname):
    if pathname == '/programs':
        return 'active'


# Main application loop
if __name__ == '__main__':
    # Uncomment this line to run the actual server
    #app.run_server(debug=False, host='166.20.109.188', port='8080')

    # Uncomment this line to debug locally
    app.run_server(debug=True, host='127.0.0.1', port='8080')
