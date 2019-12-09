from dash import exceptions
from dash.dependencies import Output, Input, State
from flask_login import current_user, login_user

import assets.SQL as sql
import pages.capacity as cap
# Import pages
import pages.employees as emp
import pages.home as home
import pages.programs as pgm
from server import app


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/employees':
        # if current_user.is_authenticated:
        #     return emp.admin_employee_page()
        # else:
        return emp.employee_page_layout()
    if pathname == '/programs':
        return pgm.Programs()
    if pathname == '/capacity':
        return cap.capacity()
    if pathname == '/':
        return home.Home()


# These callbacks just set the active class for the navbar so it colors properly
@app.callback(
    Output('homeLink', 'className'),
    [Input('url', 'pathname')])
def home_link(pathname):
    """
    This highlights the home button on the navbar if on the home page url
    :param pathname: str
    :return: str
    """
    if pathname == '/':
        return 'active'


@app.callback(
    Output('empLink', 'className'),
    [Input('url', 'pathname')])
def emp_link(pathname):
    """
    This highlights the employees button on the navbar if on the employees page url
    :param pathname: str
    :return: str
    """
    if pathname == '/employees':
        return 'active'


@app.callback(
    Output('pgmLink', 'className'),
    [Input('url', 'pathname')])
def pgm_link(pathname):
    """
    This highlights the programs button on the navbar if on the programs page url
    :param pathname: str
    :return: str
    """
    if pathname == '/programs':
        return 'active'


@app.callback(
    Output('capLink', 'className'),
    [Input('url', 'pathname')])
def cap_link(pathname):
    """
    This highlights the capacity button on the navbar if on the capacity page url
    :param pathname: str
    :return: str
    """
    if pathname == '/capacity':
        return 'active'


@app.callback(Output('loginView', 'style'),
              [Input('loginOpen', 'n_clicks'),
               Input('loginClose', 'n_clicks')])
def show_login(open_login, close_login):
    """
    This controls the display of the login modal
    :param open_login: int
    :param close_login: int
    :return: dict
    """
    if (open_login + close_login) % 2 == 0:
        return {'display': 'none'}
    return {'display': 'block'}


@app.callback([Output('loginMessage', 'children'),
               Output('loginUsername', 'value'),
               Output('loginPassword', 'value')],
              [Input('loginSubmit', 'n_clicks')],
              [State('loginUsername', 'value'),
               State('loginPassword', 'value')])
def login_message(login_click, username, password):
    """
    This controls the login submission. It passes the entered username and password to the SQL.py verify password method.
    This also controls the closing of the login modal
    :param login_click: int
    :param username: set
    :param password: set
    :return: str
    """
    if not login_click:
        raise exceptions.PreventUpdate
    result = sql.verify_password(username, password)
    return [result, '', '']


@app.callback(Output('registerModal', 'style'),
              [Input('registerOpen', 'n_clicks'),
               Input('registerClose', 'n_clicks')])
def show_registration(open_registration, close_registration):
    """
    This controls the display of the register user modal
    :param open_registration: int
    :param close_registration: int
    :return: dict
    """
    if (open_registration + close_registration) % 2 == 0:
        return {'display': 'none'}
    return {'display': 'block'}


@app.callback([Output('registerMessage', 'children'),
               Output('emp-num-dropdown', 'value'),
               Output('registerPassword', 'value'),
               Output('registerPassword2', 'value')],
              [Input('registerSubmit', 'n_clicks')],
              [State('registerUsername', 'value'),
               State('emp-num-dropdown', 'value'),
               State('registerPassword', 'value'),
               State('registerPassword2', 'value')])
def submit_registration(submit_clicks, username, emp_name, password, password2):
    """
    Submits the user regisration using the entered data
    :param submit_clicks: int
    :param username: str
    :param emp_name: str
    :param password: str
    :param password2: str
    :return: dict
    """
    if not submit_clicks:
        raise exceptions.PreventUpdate
    msg = sql.register_user(username, emp_name, password, password2)
    return [msg, emp_name, '', '']
