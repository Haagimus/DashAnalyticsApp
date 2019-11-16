import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from server import app
from .callbacks import HomeLink, EmpLink, PgmLink, CapLink
from assets.SQL import GetTable


# When new pages are added, update list with href to location
def Navbar():
    navbar = html.Div([
        html.Ul([
            html.Li(
                [html.Img(id='logo', src='..\\assets\images\L3Harris.svg')]),
            html.Li(
                [dcc.Link('Home', id='homeLink', href='/')]),
            html.Li(
                [dcc.Link('Employee', id='empLink', href='/employees')]),
            html.Li(
                [dcc.Link('Programs', id='pgmLink', href='/programs')]),
            html.Li(
                [dcc.Link('Capacity', id='capLink', href='/capacity')]),
            html.Ul(id='navRight', children=[
                html.Li(
                    [html.Button('Register', id='registerOpen', n_clicks=0)]),
                html.Li(
                    [html.Button('Login', id='loginOpen', n_clicks=0)])
            ])
        ]),
        login_modal,
        registation_modal
    ])

    return navbar


# The login modal page layout
login_modal = html.Div([
    html.Div([
        html.P(children=[''], id='loginMessage'),
        html.H3('Please log in:', id='loginHead'),
        html.P(children=['Username: ',
                         dcc.Input(type='text',
                                   id='loginUsername',
                                   className='required username',
                                   required=True,
                                   placeholder='username')]),
        html.P(children=['Password: ',
                         dcc.Input(type='password',
                                   id='loginPassword',
                                   className='required password',
                                   required=True,
                                   placeholder='password')]),
        html.Button('Login', id='loginSubmit', n_clicks=0),
        html.Button('Close', id='loginClose', n_clicks=0)
    ],
        className='modal-content')
],
    id='loginView',
    className='modal')

empNumList = GetTable('EmployeeNumbers')

# The registration modal page layout
registation_modal = html.Div([
    html.Div([
        html.H1('Register new user:'),
        html.Div([
            html.P(children=['Username: ',
                             dcc.Input(type='text',
                                       id='registerUsername',
                                       className='required username',
                                       required=True,
                                       placeholder='username')]),
            html.P(children=['Employee #: ',
                             dcc.Dropdown(id='emp-num-drowpdown',
                                          options=[{'label': i, 'value': i}
                                                   for i in empNumList.values[0]],
                                          multi=False,
                                          searchable=True)],
                   id='dropdown'),
            html.P(children=['Password: ',
                             dcc.Input(type='password',
                                       id='registerPassword',
                                       className='required password',
                                       required=True,
                                       placeholder='password')]),
            html.P(children=['Re-enter Password',
                             dcc.Input(type='password',
                                       id='registerPassword2',
                                       required=True,
                                       className='required password',
                                       placeholder='Re-enter password')]),
            html.Button('Register', id='registerSubmit', n_clicks=0),
            html.Button('Close', id='registerClose', n_clicks=0)
        ],
            id='register-form')
    ],
        className='register-modal')
],
    id='registerModal',
    className='modal')
