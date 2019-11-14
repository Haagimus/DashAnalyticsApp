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
        dcc.Input(id='email',
                  type="email",
                  placeholder="Enter your email address",
                  required=True,
                  style={'width': '400px', 'marginTop': '3%'}
                  )
    ],
        className="mr-2",
    ),
    dbc.FormGroup([
        dbc.Label("Choose one", style={'color': 'white'}),
        dbc.RadioItems(options=[
            {"label": "Report a Bug", "value": "1", "checked": ""},
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
                     placeholder="Enter comments/suggestions",
                     style={'width': '400px', 'height': '200px'},
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
    smtp_server = "frxsv-globemaster"
    sender_email = "FRX.DevOps@L3Harris.com"
    receiver_email = ['stephen.french@l3harris.com',
                      'gary.haag@l3harris.com', orig_from]
    message = """
    Subject: {0} has submitted a {1}
    Submission: {2}. """.format(sender_email, msgType, body)
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
def send_submission(msgType_value, comment_value, n_clicks, email_value):
    count = 0
    if n_clicks > 0 and n_clicks < 2:
        while count < 1:
            if msgType_value == "1":
                msgType = "Bug Report"
            elif msgType_value == "2":
                msgType = "Feature Request"
            elif msgType_value == "3":
                msgType = "Admin Request"
            subject = "A new " + msgType + " was submtited."
            body = comment_value
            if send_mail(email_value, subject, body, msgType):
                return "Message sent successfully"
            else:
                return "Message unable to send. Try resetting form"
            count = 1


@app.callback(Output('submit', 'n_clicks'),
              [Input('reset', 'n_clicks')])
def update(reset):
    return 0
