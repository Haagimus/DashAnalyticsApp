import smtplib

import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd


def read_active_features():
    '''
    Parses the text from the Active_Features text file and generates bullet points for the home page
    :return: dbc.CardBody
    '''
    af = pd.read_csv('assets/files/Active_Features.txt', sep="\n", header=None)

    return html.Ul([
        html.Li(line) for line in af[0]
    ])


def read_upcoming_features():
    '''
    Parses the text from the Upcoming_Features text file and generates bullet points for the home page
    :return: dbc.CardBody
    '''
    uf = pd.read_csv('assets/files/Upcoming_Features.txt', sep="\n", header=None)

    return html.Ul([
        html.Li(line) for line in uf[0]
    ])


# TODO: Make page content reload each time the site is visited
form = html.Content(
    dbc.Row([
        # In Development Features Column
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H5('Features in Development', className='card-title')),
                dbc.CardBody(read_upcoming_features())
            ]),
            xl=4,
            md=6,
            width=12),
        # Implemented Features Column
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H5('Implemented Features', className='card-title')),
                dbc.CardBody(read_active_features())
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
                            dbc.Input(id='email',
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
                        dbc.Textarea(id="comment", bs_size="lg",
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


def home_page_layout():
    content = html.Div(
        form,
    )
    return content


def send_mail(orig_from, subject, body, msgType):
    """

    :param orig_from: str
    :param subject: str
    :param body: str
    :param msgType: str
    :return: bool
    """
    port = 25
    smtp_server = "frxsv-globemaster"
    sender_email = "FRX.DevOps@L3Harris.com"
    receiver_email = ['stephen.french@l3harris.com',
                      'gary.haag@l3harris.com', orig_from]
    message = """Subject: {0} has submitted a {1}
    Submission: {2}. """.format(orig_from, msgType, body)
    try:
        # TODO: fix the message body and subject layout
        server = smtplib.SMTP(smtp_server, port)
        server.login("FRX.EmailRelay@iss.l3t.com", "N)QQH3hppTrthKQN")
        for email in receiver_email:
            server.sendmail(from_addr=sender_email, to_addr=email, msg=message)
        server.quit()
        return True
    except Exception as e:
        # Message send failed, returning false
        return False

#
# @app.callback(Output('loginView', 'is_open'),
#               [Input('loginOpen', 'n_clicks'),
#                Input('loginClose', 'n_clicks')],
#               [State('loginView', 'is_open')])
# def toggle_login(open_login, close_login, is_open):
#     """
#     This controls the display of the login modal
#     :param open_login: int
#     :param close_login: int
#     :return: dict
#     """
#     if open_login or close_login:
#         return not is_open
#     return is_open
