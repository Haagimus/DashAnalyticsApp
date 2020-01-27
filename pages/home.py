import smtplib
from email.message import EmailMessage

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd


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


# TODO: Make page content reload each time the site is visited
def home_page_layout():
    content = html.Div(
        html.Content(
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
                        dbc.Form(children=[
                            html.H2("User Submission Form",
                                    style={'text-align': 'center'}),
                            # Email input field
                            dbc.FormGroup([
                                dbc.Label('Email:', width=2),
                                dbc.Col(
                                    dbc.Input(id='from_addr',
                                              type="email",
                                              placeholder="Enter your L3Harris email address",
                                              value=''),
                                    width=10
                                ),
                                dbc.FormFeedback(valid=True),
                                dbc.FormFeedback(valid=False)
                            ],
                                row=True),
                            dbc.FormGroup([
                                dbc.Label("Choose one", width=4),
                                dbc.Col(
                                    dbc.Select(options=[
                                        {"label": "Report a Bug", "value": "1"},
                                        {"label": "Feature Request", "value": "2"},
                                        {"label": "Request Admin", "value": "3"}
                                    ],
                                        id='msgType',
                                        value=1
                                    ),
                                    width=8
                                )],
                                row=True
                            ),
                            dbc.FormGroup([
                                dbc.Textarea(id="body", bs_size="lg",
                                             placeholder="Enter comments/suggestions",
                                             style={'height': '200px'},
                                             value='')
                            ]),
                            dbc.FormGroup([
                                dbc.Button("Submit",
                                           id='submit',
                                           n_clicks=0,
                                           size='lg',
                                           color='success',
                                           style={'width': '100px'}),
                                dbc.Button("Reset",
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
        )
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
    smtp_server = "frxsv-globemaster"
    relay_addr = "FRX Analytics Page"
    to_addrs = ['stephen.french@l3harris.com',
                'gary.haag@l3harris.com',
                from_addr]
    msg = EmailMessage()
    msg['from'] = relay_addr
    msg['to'] = to_addrs
    msg['subject'] = subject
    msg.set_content(body)

    server = smtplib.SMTP(smtp_server, port)
    server.login("FRX.EmailRelay@iss.l3t.com", "N)QQH3hppTrthKQN")
    server.send_message(msg)
    server.quit()
