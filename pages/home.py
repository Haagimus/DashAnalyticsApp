import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from server import app
import smtplib

#  inProgress =

form = dbc.Row([
    # Features in Development Column
    dbc.Col([html.H1('Features in Development',
                     style={'color': 'white',
                            'text-align': 'center'}),
             dbc.Card(
                 dbc.CardBody([
                     html.P('''This is where the in development feature list will go. Probably add
                some descriptive text for the items as well.''')
                 ])
             )],
            width=4),
    # Implemented Features Column
    dbc.Col([html.H1('Implemented Features',
                     style={'color': 'white',
                            'text-align': 'center'}),
             dbc.Card(
                 dbc.CardBody([
                     html.P('Employee roster page')
                 ])
             )],
            width=4),
    # User Submission Form Column
    dbc.Col([
        html.Div([
            dbc.Form(children=[
                html.H1("User Submission Form",
                        style={'color': 'white',
                               'text-align': 'center'}),
                # Email input field
                dbc.FormGroup([
                    dbc.Input(id='email',
                              type="email",
                              placeholder="Enter your email address",
                              style={'width': '100%', 'marginTop': '3%'},
                              value=''),
                    dbc.FormText('Please enter your L3Harris email'),
                    dbc.FormFeedback(valid=True),
                    dbc.FormFeedback(valid=False)
                ]),
                dbc.Row([
                    dbc.Col(
                        html.H4("Choose one", style={'color': 'white'}),
                        width=3
                    ),
                    dbc.Col(
                        dbc.Select(options=[
                            {"label": "Report a Bug", "value": "1"},
                            {"label": "Feature Request", "value": "2"},
                            {"label": "Request Admin", "value": "3"}
                        ],
                            id='msgType',
                            # style={'color': 'white'}
                        ),
                        width=9
                    )]
                ),
                html.Br(),
                dbc.FormGroup([
                    dbc.Textarea(id="comment", bs_size="lg",
                                 placeholder="Enter comments/suggestions",
                                 style={'height': '200px'},
                                 value='')
                ]),
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
            html.Div(id='output-state', children=[''])],
            id='submission-form'
        )],
        width=4
    )
])


def Home():
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
        server = smtplib.SMTP(smtp_server, port)
        server.login("FRX.EmailRelay@iss.l3t.com", "N)QQH3hppTrthKQN")
        for email in receiver_email:
            server.sendmail(from_addr=sender_email, to_addr=email, msg=message)
        server.quit()
        return True
    except Exception as e:
        # Message send failed, returning false
        return False


@app.callback(Output('output-state', 'children'),
              [Input('msgType', 'value'),
               Input('comment', 'value'),
               Input('submit', 'n_clicks'),
               Input('email', 'value')])
def send_submission(msgType_value, comment_value, send, email_value):
    if send:
        if msgType_value == "1":
            msgType = "Bug Report"
        elif msgType_value == "2":
            msgType = "Feature Request"
        elif msgType_value == "3":
            msgType = "Admin Request"
        subject = "A new " + msgType + " was submtited."
        body = comment_value
        if send_mail(email_value, subject, body, msgType):
            # TODO: reset the email submission form and click count
            return "Message sent successfully"
        else:
            return "Message unable to send. Try resetting form"

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


@app.callback(Output('submit', 'n_clicks'),
              [Input('reset', 'n_clicks')])
def update(reset):
    return 0


@app.callback([Output('email', 'valid'),
               Output('email', 'invalid')],
              [Input('email', 'value')],
              )
def check_email(text):
    if text:
        is_l3harris = str.lower(text).endswith('@l3harris.com')
        return is_l3harris, not is_l3harris
    return False, False
