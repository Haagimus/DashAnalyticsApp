import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from server import app
from .callbacks import HomeLink, EmpLink, PgmLink, CapLink


# When new pages are added, update list with href to location
def Navbar():
    navbar = html.Div([
        html.Ul([
            html.Li([html.Img(id='logo', src='..\\assets\images\L3Harris.svg')]),
            html.Li([dcc.Link('Home', id='homeLink', href='/home')]),
            html.Li([dcc.Link('Employee', id='empLink', href='/employees')]),
            html.Li([dcc.Link('Programs', id='pgmLink', href='/programs')]),
            html.Li([dcc.Link('Capacity', id='capLink', href='/capacity')]),
            html.Ul(id='navRight', children=[
                html.Li([dcc.Link('Register', id='register')]),
                html.Li([html.Button('Login', id='login', n_clicks=0)])
            ])
        ]),
        html.Div([
            html.Div([
                html.P('Some text'),
                html.Button('Login', id='submit', n_clicks=0),
                html.Button('Close', id='close', n_clicks=0)
            ],
                className='modal-content')
        ],
            id='myModal',
            className='modal')
    ])

    return navbar
