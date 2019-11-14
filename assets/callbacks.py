from server import app
from dash.dependencies import Output, Input, State
from dash import dependencies
from dash.development.base_component import Component
from dash import exceptions

# Import pages
import pages.employees as emp
import pages.programs as pgm
import pages.home as home
import pages.capacity as cap
import pages.login as log
import assets.SQL as sql


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        return emp.Employees()
    if pathname == '/programs':
        return pgm.Programs()
    if pathname == '/capacity':
        return cap.Capacity()
    if pathname == '/':
        return home.Home()


# These callbacks just set the active class for the navbar so it colors
# properly
@app.callback(
    Output('homeLink', 'className'),
    [Input('url', 'pathname')])
def HomeLink(pathname):
    if pathname == '/':
        return 'active'


@app.callback(
    Output('empLink', 'className'),
    [Input('url', 'pathname')])
def EmpLink(pathname):
    if pathname == '/employees':
        return 'active'


@app.callback(
    Output('pgmLink', 'className'),
    [Input('url', 'pathname')])
def PgmLink(pathname):
    if pathname == '/programs':
        return 'active'


@app.callback(
    Output('capLink', 'className'),
    [Input('url', 'pathname')])
def CapLink(pathname):
    if pathname == '/capacity':
        return 'active'


@app.callback(Output('myModal', 'style'),
              [Input('login', 'n_clicks'),
               Input('close', 'n_clicks')])
def show(openLogin, closeLogin):
    if (openLogin + closeLogin) % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback([Output('loginMessage', 'children'),
               Output('username', 'value'),
               Output('password', 'value')],
              [Input('login-modal', 'n_clicks'),
               Input('close', 'n_clicks')],
              [State('username', 'value'),
               State('password', 'value')])
def loginMessage(loginClick, closeClick, username, password):
    # Prevent updates from happening if the login button is not clicked
    if not loginClick:
        raise exceptions.PreventUpdate
    # TODO: Create a method inside the SQL.py to authenticate users
    result = sql.verify_password(username, password)
    return [result, '', '']
