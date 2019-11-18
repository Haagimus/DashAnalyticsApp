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


@app.callback(Output('loginView', 'style'),
              [Input('loginOpen', 'n_clicks'),
               Input('loginClose', 'n_clicks')])
def showLogin(openLogin, closeLogin):
    if (openLogin + closeLogin) % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback([Output('loginMessage', 'children'),
               Output('loginUsername', 'value'),
               Output('loginPassword', 'value')],
              [Input('loginSubmit', 'n_clicks'),
               Input('loginClose', 'n_clicks')],
              [State('loginUsername', 'value'),
               State('loginPassword', 'value')])
def loginMessage(loginClick, closeClick, username, password):
    # Prevent updates from happening if the login button is not clicked
    if not loginClick:
        raise exceptions.PreventUpdate
    result = sql.verify_password(username, password)
    return [result, '', '']


@app.callback([Output('registerModal', 'style'),
               Output('registerUsername', 'value'),
               Output('emp-num-drowpdown', 'value'),
               Output('registerPassword', 'value'),
               Output('registerPassword2', 'value')],
              [Input('registerOpen', 'n_clicks'),
               Input('registerClose', 'n_clicks'),
               Input('registerSubmit', 'n_clicks')],
              [State('registerUsername', 'value')])
def showRegistration(openRegister, closeRegister, registerSubmit, username):
    if (openRegister + closeRegister) % 2 == 0:
        return [{'display': 'none'}, '', '', '', '']
    else:
        return [{'display': 'block'}, username, '', '', '']
    # TODO:  call the registration method from SQL.py
