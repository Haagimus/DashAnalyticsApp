import time

from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable

import assets.SQL as sql
from assets.navbar import navbar
from assets.models import EmployeeData, RegisteredUser
from pages import home, employees, programs, capacity
from server import app

page_list = ['', 'employees', 'programs', 'capacity']


# These callbacks handle main page functionality like content loading
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def display_page(pathname, data):
    if pathname == '/':
        return home.home_page_layout()
    if pathname == '/employees':
        try:
            return employees.employee_page_layout(data)
        except TypeError:
            return employees.employee_page_layout()
    if pathname == '/programs':
        return programs.program_page_layout()
    if pathname == '/capacity':
        return capacity.capacity_page_layout()


# @app.callback(Output('url', 'pathname'),
#               [Input('logout-button', 'n_clicks')],
#               [State('url', 'pathname'),
#                State('session-store', 'data')])
# def logout(logout_click, url, data):
#     if not logout_click:
#         raise PreventUpdate
#     data = None
#     logout(url, data)
#     return


@app.callback([Output('navbar-container', 'children'),
               Output('home-link', 'active'),
               Output('employees-link', 'active'),
               Output('programs-link', 'active'),
               Output('capacity-link', 'active')],
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def load_navbar(pathname, data):
    active_link = ([pathname == f'/{i}' for i in page_list])
    if pathname == '/':
        return [navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]]
    if pathname == '/employees':
        return [navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]]
    if pathname == '/programs':
        return [navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]]
    if pathname == '/capacity':
        return [navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]]


@app.callback(Output('loginView', 'is_open'),
              [Input('loginOpen', 'n_clicks'),
               Input('loginClose', 'n_clicks')],
              [State('loginView', 'is_open')])
def toggle_login(open_login, close_login, is_open):
    """
    This controls the display of the login modal
    :param open_login: int
    :param close_login: int
    :param is_open: bool
    :return: dict
    """
    if open_login or close_login:
        return not is_open
    return is_open


@app.callback([Output('loginMessage', 'children'),
               Output('loginMessage', 'color'),
               Output('loginMessage', 'is_open'),
               Output('loginUsername', 'value'),
               Output('loginPassword', 'value'),
               Output('session-store', 'data'),
               Output('url', 'pathname')],
              [Input('loginSubmit', 'n_clicks_timestamp'),
               Input('logout-button', 'n_clicks_timestamp')],
              [State('loginUsername', 'value'),
               State('loginPassword', 'value'),
               State('session-store', 'data'),
               State('url', 'pathname')])
def login_message(login_click, logout_click, username, password, data, path):
    """
    This controls the login submission. It passes the entered username and password to the SQL.py verify password method.
    This also controls the closing of the login modal
    :param login_click: int
    :param username: set
    :param password: set
    :param data: dict
    :param path: str
    :return: tuple
    """
    if not (login_click or logout_click):
        print('nothing clicked')
        raise PreventUpdate

    if login_click > logout_click:
        print('login clicked')
    elif logout_click > login_click:
        print('logout clicked')

    if logout_click:
        data = None
        return ['Logout successful', True, 'success', '', '', data, path]

    result = sql.verify_password(username, password)
    if type(result) == RegisteredUser:
        user = '{}, {}'.format(result.employee.employee_data[0].name_last, result.employee.employee_data[0].name_first)
        data = {'isadmin': result.employee.employee_data[0].is_admin,
                'logged_in': True,
                'login_user': user}
        result = 'Logged in as {0}'.format(result.username)
        return [result, 'success', True, '', '', data, path]
    return [result, 'danger', True, '', '', data, path]


@app.callback(Output('registerView', 'is_open'),
              [Input('registerOpen', 'n_clicks'),
               Input('registerClose', 'n_clicks')],
              [State('registerView', 'is_open')])
def toggle_registration(open_registration, close_registration, is_open):
    """
    This controls the display of the register user modal
    :param open_registration: int
    :param close_registration: int
    :param is_open: bool
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
def filter_employees(search_click, search_clear, filter_text, data):
    """
    Runs a filter query against the employees table
    :param search_click: int
    :param search_clear: int
    :param filter_text: str
    :param data: dict
    :return: DataTable
    """
    if int(search_click) > int(search_clear):
        data_set = sql.query_rows(EmployeeData, filter_text)
    elif int(search_clear) > int(search_click):
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''
    else:
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''

    if data is not None and data['isadmin']:
        # This is the admin layout
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Employee #', 'id': 'employee_number'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'},
                   {'name': 'End Date', 'id': 'date_end'}]
    else:
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Employee #', 'id': 'employee_number'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'}]

    if data is not None and data['isadmin']:
        # This is the admin layout
        data = [{'name_first': i.name_first,
                 'name_last': i.name_last,
                 'employee_number': i.employee_number,
                 'function': i.assigned_function,
                 'job_code': i.job_code,
                 'programs': i.programs,
                 'date_start': i.date_start,
                 'date_end': i.date_end} for i in data_set]
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


@app.callback([Output('employee-loading-output', 'children')],
              [Input('page-content', 'value')])
def employees_loading(value):
    time.sleep(1)
    return value
