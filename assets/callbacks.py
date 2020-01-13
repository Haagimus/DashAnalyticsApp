import time

from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable

import assets.SQL as sql
from assets.navbar import navbar
from assets.models import EmployeeData, RegisteredUser, Functions, Program
from pages import home, employees, programs, capacity
from server import app, log_time

page_list = ['', 'employees', 'programs', 'capacity']


# These callbacks handle main page functionality like content loading
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def display_page(pathname, data):
    if pathname == '/':
        return home.home_page_layout()
    if pathname == '/employees':
        return employees.employee_page_layout(data)
    if pathname == '/programs':
        return programs.program_page_layout()
    if pathname == '/capacity':
        return capacity.capacity_page_layout()


@app.callback([Output('navbar-container', 'children'),
               Output('home-link', 'active'),
               Output('employees-link', 'active'),
               Output('programs-link', 'active'),
               Output('capacity-link', 'active')],
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def load_navbar(pathname, data):
    active_link = ([pathname == f'/{i}' for i in page_list])
    return navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]


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
    :param logout_click: int
    :param username: set
    :param password: set
    :param data: dict
    :param path: str
    :return: tuple
    """
    if not (login_click or logout_click):
        raise PreventUpdate

    if login_click > logout_click:
        pass
    elif logout_click > login_click:
        pass

    if logout_click:
        app.logger.info('INFO: {} logged out successfully at {}.'.format(data['login_user'], log_time))
        data = None
        return ['Logout successful', True, 'success', '', '', data, path]

    result = sql.verify_password(username, password)
    if type(result) == RegisteredUser:
        employee = sql.query_rows(result.employee_number.number)
        user = '{}, {}'.format(employee[0].name_last, employee[0].name_first)
        data = {'isadmin': employee[0].is_admin,
                'logged_in': True,
                'login_user': user}
        result = 'Logged in as {0}'.format(result.username)
        app.logger.info('INFO: {} logged in successfully at {}.'.format(data['login_user'], log_time))
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
    """
    if open_registration or close_registration:
        return not is_open
    return is_open


@app.callback([Output('first-name', 'value'),
               Output('last-name', 'value'),
               Output('employee-number', 'value'),
               Output('job-code', 'value'),
               Output('function', 'options'),
               Output('program-name', 'options'),
               Output('start-date', 'value'),
               Output('end-date', 'value'),],
              [Input('load-employee', 'n_clicks'),
               Input('Employees', 'data'),
               Input('Employees', 'selected_rows')])
def load_employee_data(load_click, row, row_idx):
    """
    This loads selected employee data into the edit fields
    :param load_click: int
    :param row: DataFrame
    :param row_idx: int
    """
    if not load_click:
        raise PreventUpdate()
#     else:
    if len(row_idx) > 0:
        f_name = row[row_idx[0]]['name_first']
        l_name = row[row_idx[0]]['name_last']
        emp_num = row[row_idx[0]]['employee_number']
        job_code = row[row_idx[0]]['job_code']
        func = row[row_idx[0]]['function']
        if len(sql.get_rows(Functions, Functions.function == func)) > 0:
            func = sql.get_rows(Functions, Functions.function == func)[0].function
        else:
            func = None
        pgm = row[row_idx[0]]['program']
        if len(sql.get_rows(Program, Program.name == pgm)) > 0:
            pgm = sql.get_rows(Program, Program.name == pgm)[0].name
        else:
            pgm = None
        start = row[row_idx[0]]['date_start']
        end = row[row_idx[0]]['date_end']

        return f_name, l_name, emp_num, job_code, func, pgm, start, end
    raise PreventUpdate


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
            msg_text = "Bug Report"
        elif msg_type == "2":
            msg_text = "Feature Request"
        elif msg_type == "3":
            msg_text = "Admin Request"
        subject = "A new " + msg_text + " was submtited."
        body = comment_value
        if home.send_mail(email_value, subject, body, msg_text):
            update(True)
            return "Message sent successfully"
        else:
            return "Message unable to send. Try resetting form"


@app.callback([Output('Employees', 'data'),
               Output('search', 'value')],
              [Input('search-button', 'n_clicks_timestamp'),
               Input('clear-search', 'n_clicks_timestamp')],
              [State('search', 'value')])
def filter_employees(search_click, search_clear, filter_text):
    """
    Runs a filter query against the employees table
    :param search_click: int
    :param search_clear: int
    :param filter_text: str
    :return: DataTable
    """
    if int(search_click) > int(search_clear):
        data_set = sql.query_rows(filter_text)
    elif int(search_clear) > int(search_click):
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''
    else:
        data_set = sql.get_rows(EmployeeData)
        filter_text = ''

    # if data is not None and data['isadmin']:
    #     # This is the admin layout
    #     columns = [{'name': 'First Name', 'id': 'name_first', "hideable": True},
    #                {'name': 'Last Name', 'id': 'name_last', "hideable": True},
    #                {'name': 'Employee #', 'id': 'employee_number', "hideable": True},
    #                {'name': 'Job Code', 'id': 'job_code', "hideable": True},
    #                {'name': 'Job Title', 'id': 'job_title', "hideable": True},
    #                {'name': 'Level', 'id': 'level', "hideable": True},
    #                {'name': 'Assigned Function', 'id': 'function', "hideable": True},
    #                {'name': 'Assigned Program(s)', 'id': 'programs', "hideable": True},
    #                {'name': 'Start Date', 'id': 'date_start', "hideable": True},
    #                {'name': 'End Date', 'id': 'date_end', "hideable": True}]
    # else:
    #     columns = [{'name': 'First Name', 'id': 'name_first', "hideable": True},
    #                {'name': 'Last Name', 'id': 'name_last', "hideable": True},
    #                {'name': 'Employee #', 'id': 'employee_number', "hideable": True},
    #                {'name': 'Job Code', 'id': 'job_code', "hideable": True},
    #                {'name': 'Assigned Function', 'id': 'function', "hideable": True},
    #                {'name': 'Assigned Program(s)', 'id': 'program', "hideable": True},
    #                {'name': 'Start Date', 'id': 'date_start', "hideable": True}]
    #
    # if data is not None and data['isadmin']:
        # This is the admin layout
    data = [{'name_first': i.name_first,
             'name_last': i.name_last,
             'employee_number': i.employee_number.number,
             'job_code': i.job_code,
             'job_title': i.job_title,
             'level': i.level,
             'function': i.employee_number.assigned_functions[0].function
             if len(i.employee_number.assigned_functions) > 0 else '',
             'program': i.employee_number.assigned_programs[0].name
             if len(i.employee_number.assigned_programs) > 0 else '',
             'date_start': i.date_start,
             'date_end': i.date_end} for i in data_set]
    # else:
    #     data = [{'name_first': i.name_first,
    #              'name_last': i.name_last,
    #              'employee_number': i.employee_number.number,
    #              'function': i.employee_number.assigned_functions[0].function
    #              if len(i.employee_number.assigned_functions) > 0 else '',
    #              'job_code': i.job_code,
    #              'program': i.employee_number.assigned_programs[0].name
    #              if len(i.employee_number.assigned_programs) > 0 else '',
    #              'date_start': i.date_start} for i in data_set]
    #
    # figure = DataTable(
    #     id='Employees',
    #     columns=columns,
    #     data=data,
    #     editable=False,
    #     page_action='native',
    #     page_size=20,
    #     sort_action='native',
    #     sort_mode='multi',
    #     style_as_list_view=False,
    #     style_header={
    #         'backgroundColor': 'white',
    #         'fontWeight': 'bolder',
    #         'fontSize': '18px',
    #         'textAlign': 'center',
    #         'border-bottom': '1px solid black'
    #     },
    #     style_data_conditional=[
    #         {'if': {'row_index': 'odd'},
    #          'backgroundColor': 'rgb(248, 248, 248)'},
    #         {'border-bottom': '1px solid #ddd'},
    #         {'border-left': 'none'},
    #         {'border-right': 'none'}
    #     ],
    #     style_table={
    #         'overflowX': 'scroll',
    #         'border': 'solid 1px black'
    #     },
    #     row_selectable='single',
    #     selected_rows=[]
    # )
    return data, filter_text


@app.callback([Output('employee-loading-output', 'children')],
              [Input('page-content', 'value')])
def employees_loading(value):
    time.sleep(1)
    return value


@app.callback([Output('capacity-loading-output', 'children')],
              [Input('page-content', 'value')])
def capacity_loading(value):
    time.sleep(1)
    return value
