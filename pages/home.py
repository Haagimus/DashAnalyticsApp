import smtplib
from email.message import EmailMessage

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from run import site_admin, site_admin_email


# TODO: Make some sort of a site admin section to manipulate user accounts and perform repetitive server actions


def read_active_features():
    """
    Parses the text from the Active_Features text file and generates bullet points for the home page
    :return: dbc.CardBody
    """
    af = pd.read_csv('assets/files/Active_Features.txt', sep="\n", header=None)

    return html.Ul([
        html.Li(line) for line in af[0]
    ])


def read_upcoming_features():
    """
    Parses the text from the Upcoming_Features text file and generates bullet points for the home page
    :return: dbc.CardBody
    """
    uf = pd.read_csv('assets/files/Upcoming_Features.txt', sep="\n", header=None)

    return html.Ul([
        html.Li(line) for line in uf[0]
    ])


def read_logfile():
    """
    Parses the text from the log text file
    :return: dbc.CardBody
    """
    content = ''
    try:
        af = pd.read_csv('log.txt', sep="\n", header=None)
        for line in af[0]:
            if str.startswith(line, 'Running on http://127.0.0.1:8080') or \
                    str.startswith(line, 'Debugger PIN'):
                pass
            else:
                content = f'-- {line}\n{content}'
    except pd.errors.EmptyDataError:
        content = 'Log file empty or missing, no data to show'

    return content


def home_page_layout(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}

    if data['logged_in']:
        # If you are the application admin show the log window otherwise leave it hidden
        if data['login_user'] == site_admin:
            log_display = 'grid'
        else:
            log_display = 'none'
    else:
        log_display = 'none'

    content = html.Div(
        html.Content([
            dbc.Row([
                # Log contents display
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5('Log Output',
                                    className='card-title')),
                        dcc.Textarea(
                            id='log-output',
                            value=read_logfile(),
                            readOnly=True,
                            wrap='wrap')
                    ]),
                    style={'display': log_display}
                ),
                # Site admin controls
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5('Site Admin Controls',
                                    className='card-title')),
                        dbc.CardBody(
                            # id='site_admin_controls')
                            id='site-admin-card',
                            children=[dcc.Tabs(
                                id='site-admin-tabs',
                                value='current_admins_list',
                                children=[
                                    dcc.Tab(label='Current Admins',
                                            value='current_admins_list',
                                            style={'border-radius': '15px 0px 0px 0px'}),
                                    dcc.Tab(label='Edit Admins',
                                            value='site_admin_controls',
                                            style={'border-radius': '0px 15px 0px 0px'})
                                ],
                            ),
                                html.Div(
                                    children=[
                                        dcc.Loading(id='site-admin-tabs-content',
                                                    type='default')
                                    ]
                                )
                            ]
                        )
                    ]),
                    style={'display': log_display,
                           'maxWidth': '500px',
                           'maxHeight': '32.5vh'},
                ),

            ]),
            dbc.Row([
                # In Development Features Column
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5('Features in Development',
                                    className='card-title')),
                        dbc.CardBody(
                            read_upcoming_features())
                    ]),
                    xl=4,
                    md=6,
                    width=12),
                # Implemented Features Column
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.H5('Implemented Features',
                                    className='card-title')),
                        dbc.CardBody(
                            read_active_features())
                    ]),
                    xl=4,
                    md=6,
                    width=12),
                # User Submission Form Column
                dbc.Col([
                    html.Div([
                        dbc.Form([
                            html.H2('User Submission Form',
                                    style={'text-align': 'center'}),
                            # Email input field
                            dbc.FormGroup([
                                dbc.Label('Email:', width=2),
                                dbc.Col(
                                    dbc.Input(id='from_addr',
                                              type='email',
                                              placeholder='Enter your L3Harris email address',
                                              value=''),
                                    width=10
                                ),
                                dbc.FormFeedback(valid=True),
                                dbc.FormFeedback(valid=False)
                            ],
                                row=True),
                            dbc.FormGroup([
                                dbc.Label('Choose one', width=4),
                                dbc.Col(
                                    dbc.Select(options=[
                                        {'label': 'Report a Bug', 'value': '1'},
                                        {'label': 'Feature Request', 'value': '2'},
                                        {'label': 'Request Admin', 'value': '3'}
                                    ],
                                        id='msgType',
                                        value=1
                                    ),
                                    width=8
                                )],
                                row=True
                            ),
                            dbc.FormGroup([
                                dbc.Textarea(id='body', bs_size='lg',
                                             placeholder='Enter comments/suggestions',
                                             style={'height': '200px'},
                                             value='')
                            ]),
                            dbc.FormGroup([
                                html.Div('0',
                                         id='reset-div',
                                         style={'visibility': 'hidden'}),
                                dbc.Button('Submit',
                                           id='submit',
                                           n_clicks=0,
                                           size='lg',
                                           color='success',
                                           style={'width': '100px'}),
                                dbc.Button('Reset',
                                           id='reset',
                                           n_clicks=0,
                                           size='lg',
                                           color='danger',
                                           style={'width': '100px',
                                                  'float': 'right'})
                            ]),
                        ]),
                        html.Div(id='output-state', children=[''])],
                        id='submission-form'
                    )],
                    xl={'size': 4, 'offset': 0},
                    md={'size': 8, 'offset': 2},
                    width=12
                )
            ])
        ])
    )
    return content


def send_mail(from_addr, subject, body):
    """

    :param from_addr: str
    :param subject: str
    :param body: str
    :return: bool
    """
    port = 25
    smtp_server = 'smtp_server'
    relay_addr = 'FRX Analytics Page'
    relay_email = 'relay_email'
    to_addrs = [site_admin_email,
                from_addr]
    msg = EmailMessage()
    msg['from'] = relay_addr
    msg['to'] = to_addrs
    msg['subject'] = subject
    msg.set_content(body)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.login(relay_email, 'password')
        server.send_message(msg)
        server.quit()
        return None
    except TimeoutError as e:
        msg = f'{e.errno} :: {e.strerror}'
        return msg
