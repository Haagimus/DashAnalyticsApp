import dash_html_components as html
import dash_core_components as dcc
from server import app
from dash.dependencies import State, Output, Input
from flask import session
import datetime as dt


def Login():
    layout = html.Div(children=[
        # product header
        # html.Div(children=[
        #     html.Img(src="..\\assets\images\dog.jpg",
        #              alt="product", style={'width': '100px'})
        # ], style={'padding': 7, 'text-align': 'center'}),
        # html.Hr(style={'width': '30%'}),
        # content
        html.Div(children=[
            html.H3("Please log in", hidden=False, id="page_header"),
            # login form
            html.Form(children=[
                html.P(children=["Username: ", dcc.Input(
                    type='text', id='username', placeholder='username')]),
                html.P(children=["Password: ", dcc.Input(
                    type='password', id='password', placeholder='password')]),
                html.Button(children=['Login'],
                            type='submit', id='login_button')
            ], style={'width': '30%', 'margin': '0 auto'}, id="login_form", hidden=False)
        ], style={'display': 'block', 'text-align': 'center', 'padding': 2}),
        html.Br(),
        html.Hr(style={'width': '30%'}),
        # footer
        # html.Div(children=[
        #     html.Img(src="..\\assets\images\dog.jpg",
        #              alt="Logo", style={'width': '100px'})
        # ], style={'padding': 7, 'text-align': 'center'})
    ])
    return layout


@app.callback(Output('login_button', 'n_clicks_timestamp'),
              [Input('page_header', 'value')])
def checkLogin(n_clicks_timestamp, username, password):
    if n_clicks_timestamp > (dt.datetime.now().timestamp() - 1):
        
        if username == 'username' and password == 'password':
            return 'You have successfully logged in.'
        else:
            return 'Login failed.'
