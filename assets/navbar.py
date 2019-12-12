import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import assets.SQL as sql
import assets.models as models


# When new pages are added, update list with href to location
def navbar():
    navbar = html.Div([
        dbc.Nav([
            dbc.NavItem(html.Img(id='logo', src='..\\assets\images\L3Harris.svg')),
            dbc.NavItem(dbc.NavLink('Home', id='homeLink', href='/')),
            dbc.NavItem(dbc.NavLink('Employees', id='empLink', href='/employees')),
            dbc.NavItem(dbc.NavLink('Programs', id='pgmLink', href='/programs')),
            dbc.NavItem(dbc.NavLink('Capacity', id='capLink', href='/capacity')),
            dbc.NavItem(dbc.Button('Register', id='registerOpen', n_clicks=0,
                                   style={'width': '120px', 'margin': '0px 5px'})),
            dbc.NavItem(dbc.Button('Login', id='loginOpen', n_clicks=0,
                                   style={'width': '120px', 'margin': '0px 5px'}))
        ],
            pills=True,
            justified=True,
        ),
        # The login modal page layout
        dbc.Modal([
            dbc.ModalHeader('Please log in:', id='loginHead'),
            dbc.ModalBody([
                html.P(children=['Username: ',
                                 dbc.Input(type='text',
                                           id='loginUsername',
                                           className='required username',
                                           placeholder='username')]),
                html.P(children=['Password: ',
                                 dbc.Input(type='password',
                                           id='loginPassword',
                                           className='required password',
                                           placeholder='password')]),
                html.P(children=[''], id='loginMessage')
            ]),
            dbc.ModalFooter([
                dbc.Button('Login', id='loginSubmit', n_clicks=0),
                dbc.Button('Close', id='loginClose', n_clicks=0)
            ])
        ],
            id='loginView',
            centered=True),

        # The registration modal page layout
        dbc.Modal([
            dbc.ModalHeader('Register new user:'),
            dbc.ModalBody([
                html.P(children=['Username: ',
                                 dbc.Input(type='text',
                                           id='registerUsername',
                                           className='required username',
                                           placeholder='username')]),
                html.P(children=['Employee #: ',
                                 dbc.Select(id='emp-num-dropdown',
                                            options=[{'label': i.number, 'value': i.number}
                                                     for i in sql.get_rows(models.EmployeeNumber)],
                                            )],
                       id='dropdown'),
                html.P(children=['Password: ',
                                 dbc.Input(type='password',
                                           id='registerPassword',
                                           className='required password',
                                           placeholder='password')]),
                html.P(children=['Re-enter Password:',
                                 dbc.Input(type='password',
                                           id='registerPassword2',
                                           className='required password',
                                           placeholder='Re-enter password')]),
                html.P(children=[''], id='registerMessage')
            ]),
            dbc.ModalFooter([
                dbc.Button('Register', id='registerSubmit', n_clicks=0),
                dbc.Button('Close', id='registerClose', n_clicks=0)
            ])
        ],
            id='registerView',
            centered=True)
    ])

    return navbar
