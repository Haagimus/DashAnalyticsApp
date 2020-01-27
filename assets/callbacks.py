import time

from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_table import DataTable

import assets.SQL as sql
from assets.navbar import navbar
from assets.models import EmployeeData, RegisteredUser, Functions, Program, EmployeeFunctionLink, EmployeeProgramLink
from pages import home, employees, programs, capacity
from server import app, log_time

page_list = ['',
             'employees',
             'programs',
             'capacity']

data_fields = ['name_first',
               'name_last',
               # 'employee_number',
               'job_code',
               'level',
               'function',
               'programs',
               'date_start',
               'date_end']


# region Application callbacks
# region Page display callback
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


# endregion


# region Navbar state callback
@app.callback([Output('navbar-container', 'children'),
               Output('home-link', 'active'),
               Output('employees-link', 'active'),
               Output('programs-link', 'active'),
               Output('capacity-link', 'active')],
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def navbar_state(pathname, data):
    active_link = ([pathname == f'/{i}' for i in page_list])
    return navbar(data), active_link[0], active_link[1], active_link[2], active_link[3]


# endregion
# endregion


# region Home Page callbacks
# region Login modal callback
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


# endregion


# region Login alert message callback
@app.callback([Output('alert_toast', 'children'),
               Output('alert_toast', 'color'),
               Output('alert_toast', 'is_open'),
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

    if logout_click:
        app.logger.info('INFO: {} logged out successfully at {}.'.format(data['login_user'], log_time))
        data = None
        # alert_message('Logout successful', 'success')
        return ['Logout successful', 'success', True, '', '', data, path]

    result = sql.verify_password(username, password)
    if type(result) == RegisteredUser:
        employee = sql.query_rows(result.employee_number.number)
        user = '{}, {}'.format(employee[0].name_last, employee[0].name_first)
        data = {'isadmin': employee[0].is_admin,
                'logged_in': True,
                'login_user': user}
        result = 'Logged in as {0}'.format(result.username)
        app.logger.info('INFO: {} logged in successfully at {}.'.format(data['login_user'], log_time))
        # alert_message(result, 'success')
        return [result, 'success', True, '', '', data, path]
    # alert_message(result, 'danger')
    return [result, 'danger', True, '', '', data, path]


# endregion


# region Registration display callback
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


# endregion


# region Registration submit callback
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


# endregion


# region Email reset callback
@app.callback([Output('email', 'value'),
               Output('msgType', 'value'),
               Output('comment', 'value')],
              [Input('reset', 'n_clicks')])
def reset_email_form(reset_click):
    if reset_click:
        return ['', 1, '']
    return ['', '', '']


# endregion


# region Email validation callback
@app.callback([Output('email', 'valid'),
               Output('email', 'invalid')],
              [Input('email', 'value')])
def email_validity_checker(text):
    if text:
        is_l3harris = str.lower(text).endswith('@l3harris.com')
        return is_l3harris, not is_l3harris
    return False, False


# endregion


# region Send email callback
@app.callback(Output('output-state', 'children'),
              [Input('msgType', 'value'),
               Input('body', 'value'),
               Input('submit', 'n_clicks'),
               Input('from_addr', 'value')])
def send_email(msg_type, body, send, from_addr):
    if send:
        msg_text = ''
        if msg_type == "1":
            msg_text = "Bug Report"
        elif msg_type == "2":
            msg_text = "Feature Request"
        elif msg_type == "3":
            msg_text = "Admin Request"
        subject = "A new " + msg_text + " was submitted."
        body = body
        result = home.send_mail(from_addr, subject, body)
        if result is True:
            reset_email_form(True)
            return "Message sent successfully"
        elif isinstance(result, Exception):
            return result.strerror
        elif isinstance(result, str):
            return result

# endregion
# endregion


# region Employee Page callbacks
# region Employee editor data loading callback
@app.callback([Output('first-name', 'value'),
               Output('last-name', 'value'),
               Output('employee-number', 'value'),
               Output('job-code', 'value'),
               Output('level', 'value'),
               Output('function', 'value'),
               Output('program-name', 'value'),
               Output('start-date', 'date'),
               Output('end-date', 'date'),
               Output('save-employee', 'disabled'),
               Output('quick-close-employee', 'disabled')],
              [Input('Employees', 'data'),
               Input('Employees', 'selected_rows')],
              [State('function', 'options'),
               State('program-name', 'options')])
def load_employee_data(row, row_idx, func_op, pgm_op):
    """
    This loads selected employee data into the edit fields
    :param row: DataFrame
    :param row_idx: int
    :param func_op: []
    :param pgm_op: []
    """
    if len(row_idx) > 0:
        quick_close_disabled = False
        save_button_disabled = False
        f_name = row[row_idx[0]]['name_first']
        l_name = row[row_idx[0]]['name_last']
        emp_num = row[row_idx[0]]['employee_number']
        job_code = row[row_idx[0]]['job_code']
        level = row[row_idx[0]]['level']
        try:
            func = [f for f in func_op if row[row_idx[0]]['function'] == f['label']][0]['value']
        except IndexError:
            func = None

        try:
            pgm = [f for f in pgm_op if row[row_idx[0]]['programs'] == f['label']][0]['value']
        except IndexError:
            pgm = None

        start = row[row_idx[0]]['date_start']
        end = row[row_idx[0]]['date_end']

        return f_name, l_name, emp_num, job_code, level, func, pgm, start, end, quick_close_disabled, save_button_disabled
    else:
        return '', '', '', '', '', 0, 0, None, None, True, True


# endregion


# region Employee editor button functions callback
@app.callback([Output('Employees', 'selected_rows'),
               Output('Employees', 'selected_cells'),
               Output('Employees', 'data'),
               Output('search', 'value')],
              [Input('search-button', 'n_clicks_timestamp'),
               Input('clear-search', 'n_clicks_timestamp'),
               Input('new-employee', 'n_clicks_timestamp'),
               Input('save-employee', 'n_clicks_timestamp'),
               Input('quick-close-employee', 'n_clicks_timestamp'),
               Input('clear-employee-editor', 'n_clicks_timestamp')],
              [State('Employees', 'data'),
               State('Employees', 'selected_rows'),
               State('search', 'value'),
               State('first-name', 'value'),
               State('last-name', 'value'),
               State('employee-number', 'value'),
               State('job-code', 'value'),
               State('level', 'value'),
               State('function', 'value'),
               State('program-name', 'value'),
               State('start-date', 'date'),
               State('end-date', 'date'),
               State('session-store', 'data')])
def employee_editor_buttons(search_click, search_clear, new, save, close, clear, row, row_idx, search_text, first_name, last_name, employee_number, job_code,
                            level, func, pgm, start_date, end_date, data):
    # https://community.plot.ly/t/input-two-or-more-button-how-to-tell-which-button-is-pressed/5788/29
    if func != (0 or None):
        func = sql.get_rows(Functions, Functions.id == func)[0].function
    else:
        func = None

    if pgm != (0 or None):
        pgm_list = []
        for p in pgm:
            pgm_list.append(sql.get_rows(Program, Program.id == p)[0].name)
    else:
        pgm_list = None

    editor_fields = [first_name,
                     last_name,
                     # employee_number,
                     job_code,
                     level,
                     func,
                     pgm_list,
                     start_date,
                     end_date]

    new = 0 if new is None else new
    save = 0 if save is None else save
    close = 0 if close is None else close
    clear = 0 if clear is None else clear

    if new > save and new > close and new > clear:
        # New was clicked
        print('new clicked: adding new database entry')
        if first_name is '' or last_name is '' or not isinstance(employee_number, int) or job_code is '' or start_date is '':
            pass
        sql.add_employee(first_name, last_name, employee_number, job_code, level, func, pgm, start_date, end_date)
        app.logger.info(
            f'INFO: The user {data["login_user"]} added a new employee using the following information: first_name:{first_name}, last_name:{last_name}, employee_number:\
            {employee_number}, job_code:{job_code}, level:{level}, function:{func}, program:{pgm}, start_date:{start_date}, end_date:{end_date}')
    elif save > new and save > close and save > clear:
        # Save was clicked
        print('save clicked: updating database entry')
        updates_exist = False
        updated_indices = ''
        update_args = {}

        for i in range(len(data_fields)):
            if row[row_idx[0]][data_fields[i]] != editor_fields[i]:
                updates_exist = True
                update_args[data_fields[i]] = editor_fields[i]
                updated_indices += f', {data_fields[i]}: {row[row_idx[0]][data_fields[i]]} >> {editor_fields[i]}'
        if updates_exist:
            sql.update_employee(row[row_idx[0]]['employee_number'], **update_args)
            app.logger.info(
                f'INFO: The user {data["login_user"]} updated the employee record for {row[row_idx[0]]["name_first"]} {row[row_idx[0]]["name_last"]} '
                f'with the following information {updated_indices}')
    elif close > new and close > save and close > clear:
        # Close was clicked
        print('close clicked: duplicating selected database entry, closing the orginal and loading the duplicate')
    elif clear > new and clear > close and clear > close:
        # Clear was clicked
        print('clear clicked: deselecting currently active row')
    else:
        # Nothing was clicked
        print('nothing clicked: doing nothing')

    if search_click > search_clear:
        data_set = sql.query_rows(search_text)
    elif search_clear > search_click:
        data_set = sql.get_rows(EmployeeData)
        search_text = ''
    else:
        data_set = sql.get_rows(EmployeeData)
        search_text = ''

    # TODO: Add ability to comma separate multiple search criteria

    data = [{'name_first': i.name_first,
             'name_last': i.name_last,
             'employee_number': i.employee_number.number,
             'job_code': i.job_code,
             'job_title': i.job_title,
             'level': i.level,
             'function': sql.get_rows(class_name=EmployeeFunctionLink,
                                      filter_text=EmployeeFunctionLink.employee_number == i.employee_number_number)[0].employee_function
             if len(sql.get_rows(class_name=EmployeeFunctionLink,
                                 filter_text=EmployeeFunctionLink.employee_number == i.employee_number_number)) > 0 else '',
             'programs': sql.get_rows(class_name=EmployeeProgramLink,
                                      filter_text=EmployeeProgramLink.employee_number == i.employee_number_number)[0].employee_program
             if len(sql.get_rows(class_name=EmployeeProgramLink,
                                 filter_text=EmployeeProgramLink.employee_number == i.employee_number_number)) > 0 else '',
             'date_start': i.date_start,
             'date_end': i.date_end} for i in data_set]

    return row_idx, [], data, search_text


# endregion


# region Add new employee callback
@app.callback([Output('new-employee', 'disabled')],
              [Input('first-name', 'value'),
               Input('last-name', 'value'),
               Input('employee-number', 'value'),
               Input('job-code', 'value'),
               Input('start-date', 'date')])
def add_employee_button_state(first_name, last_name, employee_number, job_code, start_date):
    if first_name is '' or last_name is '' or not isinstance(employee_number, int) or job_code is '' or start_date is '':
        return [True]
    return [False]


# endregion


# region Employee data table filtering
# @app.callback([Output('Employees', 'data'),
#                Output('search', 'value')],
#               [Input('search-button', 'n_clicks_timestamp'),
#                Input('clear-search', 'n_clicks_timestamp'),
#                Input('new-employee', 'n_clicks_timestamp'),
#                Input('save-employee', 'n_clicks_timestamp'),
#                Input('quick-close-employee', 'n_clicks_timestamp')],
#               [State('search', 'value')])
# def filter_employee_data_table(search_click, search_clear, new, save, close, filter_text):
#     """
#     Runs a filter query against the employees table
#     :param search_click: int
#     :param search_clear: int
#     :param new: int
#     :param save: int
#     :param close: int
#     :param filter_text: str
#     :return: DataTable
#     """
#     new = 0 if new is None else new
#     save = 0 if save is None else save
#     close = 0 if close is None else close
#
#     if new > save and new > close:
#         # New was clicked
#         print('new clicked: reloading data')
#
#         pass
#     elif save > new and save > close:
#         # Save was clicked
#         print('save clicked: reloading data')
#
#         pass
#     elif close > new and close > save:
#         # Close was clicked
#         print('close clicked: reloading data')
#
#         pass
#     # else:
#     #     # Nothing was clicked
#     #     print('nothing clicked')
#
#     if search_click > search_clear:
#         data_set = sql.query_rows(filter_text)
#     elif search_clear > search_click:
#         data_set = sql.get_rows(EmployeeData)
#         filter_text = ''
#     else:
#         data_set = sql.get_rows(EmployeeData)
#         filter_text = ''
#
#     # TODO: Add ability to comma separate multiple search criteria
#
#     data = [{'name_first': i.name_first,
#              'name_last': i.name_last,
#              'employee_number': i.employee_number.number,
#              'job_code': i.job_code,
#              'job_title': i.job_title,
#              'level': i.level,
#              'function': sql.get_rows(class_name=EmployeeFunctionLink,
#                                       filter_text=EmployeeFunctionLink.employee_number == i.employee_number_number)[0].employee_function
#              if len(sql.get_rows(class_name=EmployeeFunctionLink,
#                                  filter_text=EmployeeFunctionLink.employee_number == i.employee_number_number)) > 0 else '',
#              'programs': sql.get_rows(class_name=EmployeeProgramLink,
#                                       filter_text=EmployeeProgramLink.employee_number == i.employee_number_number)[0].employee_program
#              if len(sql.get_rows(class_name=EmployeeProgramLink,
#                                  filter_text=EmployeeProgramLink.employee_number == i.employee_number_number)) > 0 else '',
#              'date_start': i.date_start,
#              'date_end': i.date_end} for i in data_set]
#
#     return data, filter_text


# endregion


# region Employee editor display callback
@app.callback([Output('employee-editor', 'style'),
               Output('data-container', 'style')],
              [Input('open-employee-editor', 'n_clicks_timestamp'),
               Input('close-employee-editor', 'n_clicks_timestamp')],
              [State('employee-editor', 'style'),
               State('data-container', 'style')])
def employee_editor_control(open_click, close_click, editor_state, container_state):
    if not (open_click or close_click):
        raise PreventUpdate

    editor = editor_state
    data = container_state

    if open_click > close_click:
        editor = {'width': '300px'}
        data = {'margin-right': '300px',
                'width': 'calc(100vw - 350px)'}
    elif close_click > open_click:
        editor = {'width': '0px'}
        data = {'margin-right': '0px',
                'width': '100%'}

    return [editor, data]


# endregion


# region Employee data table loading animation
@app.callback([Output('employee-loading-output', 'children')],
              [Input('page-content', 'value')])
def employees_loading_animation(value):
    time.sleep(1)
    return value


# endregion
# endregion


# region Capacity page callbacks
# region Capacity page loading animation
@app.callback([Output('capacity-loading-output', 'children')],
              [Input('page-content', 'value')])
def capacity_loading_animation(value):
    time.sleep(1)
    return value
# endregion
# endregion
