# Dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

import assets.navbar as nb
from server import app
import assets.callbacks

nav = nb.navbar()

# Layout
app.layout = html.Div([
    dcc.Store(id='session-store',
              storage_type='session'),
    dcc.Location(id='url', refresh=False),
    nav,
    dbc.Col(
        html.Div(id='page-content')
    ),
])


@app.callback(Output('session-store', 'data')
              [Input('session-store', 'data')])
def get_admin(data):
    if data is None:
        raise PreventUpdate
    data = data or {}
    return data['isadmin']
