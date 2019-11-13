import dash_html_components as html
import dash_core_components as dcc
from server import app
from dash.dependencies import State, Output, Input


def Login():
    layout = html.Div(
        children=[
            html.Hr(style={'width': '30%'}),
            # content
            html.Div(children=[
                html.H3("Please log in",
                        hidden=False,
                        id="page_header"),
                html.P(children=["Username: ",
                                 dcc.Input(type='text',
                                           id='username',
                                           placeholder='username')]),
                html.P(children=["Password: ",
                                 dcc.Input(type='password',
                                           id='password',
                                           placeholder='password')]),
                html.Button(children='Login',
                            id='submit',
                            n_clicks=0)
            ], style={'display': 'block', 'text-align': 'center', 'padding': 2}),
            html.Br(),
            html.Hr(style={'width': '30%'})
            # footer
            # html.Div(children=[
            #     html.Img(src="..\\assets\images\dog.jpg",
            #              alt="Logo", style={'width': '100px'})
            # ], style={'padding': 7, 'text-align': 'center'})
        ])
    return layout


@app.callback(Output('page-header', 'value'),
              [Input('submit', 'n_clicks')],
              [State('username', 'value'),
               State('password', 'value')])
def checkLogin(n, username, password):
    if n_clicks == 0:
        pass
    else:
        if username == 'username' and password == 'password':
            return True
        else:
            return False