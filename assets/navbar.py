import dash_bootstrap_components as dbc
import dash_html_components as html

import assets.SQL as sql
import assets.models as models


def nav_logout(lbl):
    return dbc.NavItem([
        dbc.Label('Logged in as: {}'.format(lbl),
                  style={'margin': '0px 10px'}),
        dbc.Button('Logout',
                   id='logout-button',
                   n_clicks=0,
                   n_clicks_timestamp=0,
                   style={'width': '120px',
                          'margin': '0px 5px'})],
        className='ml-auto')


nav_login = dbc.NavItem([
    dbc.Button('Register',
               id='registerOpen',
               n_clicks=0,
               style={'width': '120px',
                      'margin': '0px 5px'}),
    dbc.Button('Login',
               id='loginOpen',
               n_clicks=0,
               style={'width': '120px',
                      'margin': '0px 5px'})],
    className='ml-auto')

login_modal = dbc.Modal([
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
                                   placeholder='password')])
    ]),
    dbc.ModalFooter([
        dbc.Button('Login',
                   id='loginSubmit',
                   n_clicks=0,
                   n_clicks_timestamp=0),
        dbc.Button('Close',
                   id='loginClose',
                   n_clicks=0)
    ])
],
    id='loginView',
    centered=True)

registration_modal = dbc.Modal([
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


def navbar(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}
    if data['logged_in']:
        if data['isadmin']:
            lbl = '{} (Admin)'.format(data['login_user'])
        else:
            lbl = data['login_user']
        layout = html.Nav([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink(html.Img(id='logo', src='..\\assets\images\L3Harris.svg'),
                                        href='https://nexus.l3harris.com/SitePages/Welcome.aspx',
                                        style={'padding': '0px'})),
                dbc.NavItem(dbc.NavLink('Home', id='home-link', href='/')),
                dbc.NavItem(dbc.NavLink('Employees', id='employees-link', href='/employees')),
                dbc.NavItem(dbc.NavLink('Programs', id='programs-link', href='/programs')),
                dbc.NavItem(dbc.NavLink('Capacity', id='capacity-link', href='/capacity')),
                nav_logout(lbl)],
                pills=True,
                id='navbar')
        ])
    else:
        # TODO: Look into auto generating the options and page links based on page py files
        layout = html.Nav([
            dbc.Nav([
                dbc.NavItem(dbc.NavLink(html.Img(id='logo', src='..\\assets\images\L3Harris.svg'),
                                        href='https://nexus.l3harris.com/SitePages/Welcome.aspx',
                                        style={'padding': '0px'})),
                dbc.NavItem(dbc.NavLink('Home', id='home-link', href='/')),
                dbc.NavItem(dbc.NavLink('Employees', id='employees-link', href='/employees')),
                dbc.NavItem(dbc.NavLink('Programs', id='programs-link', href='/programs')),
                dbc.NavItem(dbc.NavLink('Capacity', id='capacity-link', href='/capacity')),
                nav_login],
                pills=True,
                id='navbar'),

            # The login modal page layout
            login_modal,

            # The registration modal page layout
            registration_modal
        ])

    return layout
