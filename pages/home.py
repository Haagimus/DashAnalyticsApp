import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from server import app
import smtplib

#  inProgress =

form = dbc.Form(children=[
    html.H1("User Submission Form", style={'color': 'white'}),
    dbc.FormGroup([
        dbc.Input(id='email', type="email", placeholder="Enter your email address",
                  style={'width': '400px', 'marginTop': '3%'}),
    ],
        className="mr-2",
    ),
    dbc.FormGroup([
        dbc.Label("Choose one", style={'color': 'white'}),
        dbc.RadioItems(options=[
            {"label": "Report a Bug", "value": "1"},
            {"label": "Feature Request", "value": "2"},
            {"label": "Request Admin", "value": "3"}
        ],
            id='msgType',
            style={'color': 'white'}
        ),
    ], className="mr-2"
    ),
    dbc.FormGroup([
        dbc.Textarea(id="comment", className="mr-2", bs_size="lg",
                     placeholder="Enter comments/suggestions", style={'width': '400px', 'height': '200px'},
                     value='')],
                  className="mr-2"),
    dbc.Button("Submit", id='submit', n_clicks=0),
    dbc.Button("Reset", id='reset', n_clicks=0),
    html.Div(id='output-state', children=[''])],
    inline=True,
    id='submission-form'
)


def Home():
    content = html.Div(className=".col-12", children=[
        form,
    ])
    return content


def send_mail(orig_from, subject, body, msgType):
    port = 25
    # uncomment below for production
    # smtp_server = "frxsv-globemaster"
    # uncomment for local testing
    smtp_server = "relay.l3t.com"
    sender_email = "FRX.DevOps@L3Harris.com"
    user = orig_from
    receiver_email = "stephen.french@l3harris.com;gary.haag@l3harris.com"
    message = """"\
    Subject: {0} has submitted a {1}


    Submission: {2}. """.format(subject, msgType, body)

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.login("FRX.EmailRelay@iss.l3t.com", "N)QQH3hppTrthKQN")
        server.sendmail(sender_email, receiver_email, message)
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
def send_submission(msgType_value, comment_value, n_clicks, email_value):
    if n_clicks > 0 and n_clicks < 2:
        if msgType_value == "1":
            msgType = "Bug Report"
        elif msgType_value == "2":
            msgType = "Feature Request"
        elif msgType_value == "3":
            msgType = "Request Admin"
        subject = "A new " + msgType + " was submtited."
        body = comment_value
        if send_mail(email_value, subject, body, msgType):
            return "Message sent successfully"
        else:
            return "Message unable to send. Try resetting form"


@app.callback(Output('submit', 'n_clicks'),
              [Input('reset', 'n_clicks')])
def update(reset):
    return 0
