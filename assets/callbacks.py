from dash import exceptions
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

import assets.SQL as sql
from pages import employees, programs, capacity, home
from server import app


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('session-store', 'data')])
def display_page(pathname, data):
    if pathname == '/employees':
        return employees.employee_page_layout(data['isadmin'])
    if pathname == '/programs':
        return programs.Programs()
    if pathname == '/capacity':
        return capacity.capacity()
    if pathname == '/':
        return home.home()


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


@app.callback(Output('loginView', 'is_open'),
              [Input('loginOpen', 'n_clicks'),
               Input('loginClose', 'n_clicks')],
              [State('loginView', 'is_open')])
def toggle_login(open_login, close_login, is_open):
    """
    This controls the display of the login modal
    :param open_login: int
    :param close_login: int
    :return: dict
    """
    if open_login or close_login:
        return not is_open
    return is_open


@app.callback([Output('loginMessage', 'children'),
               Output('loginUsername', 'value'),
               Output('loginPassword', 'value')],
              [Input('loginSubmit', 'n_clicks')],
              [State('loginUsername', 'value'),
               State('loginPassword', 'value'),
               State('session-store', 'data')])
def login_message(login_click, username, password, data):
    """
    This controls the login submission. It passes the entered username and password to the SQL.py verify password method.
    This also controls the closing of the login modal
    :param login_click: int
    :param username: set
    :param password: set
    :return: str
    """
    if not login_click:
        raise PreventUpdate
    data = {'isadmin': False}
    result = sql.verify_password(username, password)
    data['isadmin'] = result[1]
    return [result[0], '', '']


@app.callback(Output('registerView', 'is_open'),
              [Input('registerOpen', 'n_clicks'),
               Input('registerClose', 'n_clicks')],
              [State('registerView', 'is_open')])
def toggle_registration(open_registration, close_registration, is_open):
    """
    This controls the display of the register user modal
    :param open_registration: int
    :param close_registration: int
    :return: dict
    """
    if open_registration or close_registration:
        return not is_open
    return is_open


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
    Submits the user registration using the entered data
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


@app.callback([Output('email', 'value'),
               Output('msgType', 'value'),
               Output('comment', 'value')],
              [Input('reset', 'n_clicks')])
def update(reset):
    if reset:
        return ['', 1, '']
    return ['', '', '']


@app.callback([Output('email', 'valid'),
               Output('email', 'invalid')],
              [Input('email', 'value')],
              )
def check_email(text):
    if text:
        is_l3harris = str.lower(text).endswith('@l3harris.com')
        return is_l3harris, not is_l3harris
    return False, False


@app.callback(Output('output-state', 'children'),
              [Input('msgType', 'value'),
               Input('comment', 'value'),
               Input('submit', 'n_clicks'),
               Input('email', 'value')])
def send_submission(msg_type, comment_value, send, email_value):
    if send:
        if msg_type == "1":
            msgType = "Bug Report"
        elif msg_type == "2":
            msgType = "Feature Request"
        elif msg_type == "3":
            msgType = "Admin Request"
        subject = "A new " + msgType + " was submtited."
        body = comment_value
        if home.send_mail(email_value, subject, body, msgType):
            # TODO: reset the email submission form and click count
            update(True)
            return "Message sent successfully"
        else:
            return "Message unable to send. Try resetting form"
