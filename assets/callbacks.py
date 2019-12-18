import datetime

from dash import exceptions
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from dash_table import DataTable
import dash_html_components as html

import assets.SQL as sql
from pages import employees, programs, capacity, home
from assets.models import EmployeeData
from server import app


# These callbacks handle main page functionality like content loading
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('session-store', 'data')])
def display_page(pathname, admin):
    if pathname == '/employees':
        return employees.employee_page_layout(admin)
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
               Output('loginPassword', 'value'),
               Output('session-store', 'data')],
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
    return [result[0], '', '', result[1]]


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
        raise PreventUpdate
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
              [Input('email', 'value')])
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
            update(True)
            return "Message sent successfully"
        else:
            return "Message unable to send. Try resetting form"


@app.callback([Output('employee-container', 'children'),
               Output('search', 'value')],
              [Input('search-button', 'n_clicks_timestamp'),
               Input('clear-search', 'n_clicks_timestamp')],
              [State('search', 'value'),
               State('session-store', 'data')])
def filter_employees(search_click, search_clear, filter_text, admin):
    if int(search_click) > int(search_clear):
        data_set = sql.query_rows(EmployeeData, filter_text)
    elif int(search_clear) > int(search_click):
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''
    else:
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''

    if not admin:
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Employee #', 'id': 'employee_number'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'}]
    else:
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Employee #', 'id': 'employee_number'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'},
                   {'name': 'End Date', 'id': 'date_end'}]

    if not admin:
        data = [{'name_first': i.name_first,
                 'name_last': i.name_last,
                 'employee_number': i.employee_number,
                 'function': i.assigned_function,
                 'job_code': i.job_code,
                 'programs': i.programs,
                 'date_start': i.date_start} for i in data_set]
    else:
        data = [{'name_first': i.name_first,
                 'name_last': i.name_last,
                 'employee_number': i.employee_number,
                 'function': i.assigned_function,
                 'job_code': i.job_code,
                 'programs': i.programs,
                 'date_start': i.date_start} for i in data_set]

    figure = DataTable(
        id='Employees',
        columns=columns,
        data=data,
        editable=False,
        page_action='native',
        page_size=20,
        sort_action='native',
        sort_mode='multi',
        style_as_list_view=False,
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bolder',
            'fontSize': '18px',
            'textAlign': 'center',
            'border-bottom': '1px solid black'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
             'backgroundColor': 'rgb(248, 248, 248)'},
            {'border-bottom': '1px solid #ddd'},
            {'border-left': 'none'},
            {'border-right': 'none'}
        ],
        row_selectable='single'
    )
    return [figure], filter_text
