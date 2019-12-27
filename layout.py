# Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from server import app
import assets.callbacks

navbar = html.Nav(id='navbar-container')
content = html.Div(id='page-content')
footer = html.Footer(
    dbc.Alert(id='loginMessage',
              is_open=True,
              duration=4000,
              style={'position': 'fixed',
                     'bottom': 10,
                     'right': 10,
                     'width': 350,
                     'z-index': 999,
                     'text-align': 'center',
                     'vertical-align': 'middle'}))


app.layout = html.Div([
    dcc.Store(id='session-store',
              storage_type='session'),
    dcc.Location(id='url', ),
    navbar,
    content,
    footer
])
