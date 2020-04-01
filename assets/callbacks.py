import time
from datetime import date, datetime
from io import StringIO

import dash_core_components as dcc
import dash_table as dt
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dateutil.relativedelta import relativedelta

import assets.SQL as CUSTOM_SQL
from assets.models import *
from assets.navbar import navbar
from pages import home, employees, programs, capacity
from pages.programs import parse_contents
from server import app, log_time, card_style

page_list = ['',
             'employees',
             'programs',
             'capacity']

data_fields = ['name_first',
               'name_last',
               'job_code',
               'level',
               'function',
               'programs',
               'date_start',
               'date_end']

update_btn = dbc.Button('Update Entry',
                        id='update_entry',
                        color='primary')

delete_btn = dbc.Button('Delete Entry',
                        id='delete_entry',
                        color='danger')

add_btn = dbc.Button('Add Entry',
                     id='add_entry',
                     color='primary')


# region Application callbacks
# region Page display callback
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')],
              [State('session-store', 'data')])
def display_page(pathname, data):
    if pathname == '/':
        return home.home_page_layout(data)
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
    This controls the login submission. It passes the entered username and password to the SQL.py verify password method
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
        app.logger.info('INFO :: {} logged out successfully at {}.'.format(data['login_user'], log_time))
        data = None
        # alert_message('Logout successful', 'success')
        return ['Logout successful', 'success', True, '', '', data, path]

    result = CUSTOM_SQL.verify_password(username, password)
    if type(result) == RegisteredUser:
        employee = CUSTOM_SQL.query_rows(result.employee_number.number)
        user = '{}, {}'.format(employee[0].name_last, employee[0].name_first)
        data = {'isadmin': employee[0].is_admin,
                'logged_in': True,
                'login_user': user}
        result = 'Logged in as {0}'.format(result.username)
        app.logger.info('INFO :: {} logged in successfully at {}.'.format(data['login_user'], log_time))
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
    msg = CUSTOM_SQL.register_user(username, emp_name, password, password2)
    return [msg, emp_name, '', '']


# endregion


# region Email validation callback
@app.callback(Output('from_addr', 'valid'),
              [Input('from_addr', 'value')])
def email_validity_checker(text):
    is_l3harris = False
    if text:
        is_l3harris = str.lower(text).endswith('@l3harris.com')
    return is_l3harris


# endregion


# region Email form buttons
@app.callback(Output('submit', 'disabled'),
              [Input('body', 'value'),
               Input('from_addr', 'valid')])
def email_button_states(msg_text, from_valid):
    if msg_text == '' or from_valid is False:
        return True
    elif msg_text != '' and from_valid is True:
        return False


# endregion


# region Send email callback
@app.callback([Output('output-state', 'children'),
               Output('from_addr', 'value'),
               Output('msgType', 'value'),
               Output('body', 'value')],
              [Input('submit', 'n_clicks_timestamp'),
               Input('reset', 'n_clicks_timestamp')],
              [State('from_addr', 'value'),
               State('msgType', 'value'),
               State('body', 'value')])
def send_email(submit, reset, from_addr, msg_type, body):
    reset = 0 if reset is None else reset
    submit = 0 if submit is None else submit

    if reset > submit:
        return '', '', 1, ''
    elif submit > reset:
        msg_text = ''
        if msg_type == "1":
            msg_text = "Bug Report"
        elif msg_type == "2":
            msg_text = "Feature Request"
        elif msg_type == "3":
            msg_text = "Admin Request"
        subject = f"A new {msg_text} was submitted by {from_addr}"
        body = body
        result = home.send_mail(from_addr, subject, body)
        if result is None:
            return "Message sent successfully", '', 1, ''
        else:
            return result, '', 1, ''


# endregion


# region Site admin card
@app.callback(Output('site-admin-tabs-content', 'children'),
              [Input('site-admin-tabs', 'value')])
def site_admin_card(tab):
    time.sleep(1)
    if tab == 'current_admins_list':
        # noinspection PyPep8
        admins = CUSTOM_SQL.get_rows(EmployeeData, EmployeeData.is_admin == True)
        columns = [{'name': 'Name', 'id': 'name'},
                   {'name': 'Function', 'id': 'function'}]
        data = [{'name': f'{i.name_last}, {i.name_first}',
                 'function': i.job_title} for i in admins]
        return dt.DataTable(
            id='admins-viewer',
            data=data,
            columns=columns,
            fill_width=True,
            sort_action='native',
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'rgb(230, 230 ,230)',
                'textAlign': 'center'
            },
            style_data={
                'whiteSpace': 'normal'
            },
            style_table={
                'padding': '0px 15px',
                'maxHeight': '23vh',
                'overflowX': 'auto',
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'},
                 'backgroundColor': 'rgb(221, 235, 247)'}
            ]
        )
    elif tab == 'site_admin_controls':
        data = CUSTOM_SQL.get_rows(EmployeeData, distinct=True)

        employee_select = dbc.FormGroup([
            dbc.Label('Employee Name:', width=4),
            dbc.Col(
                dcc.Dropdown(
                    id='user_list',
                    options=[{'label': f'{i.name_last}, {i.name_first}',
                              'value': i.employee_number_number} for i in data if i.date_end is None],
                    clearable=True,
                    multi=False
                )
            )
        ],
            row=True
        )

        employee_number = dbc.FormGroup([
            dbc.Label('Employee Number:', width=4),
            dbc.Col(
                dbc.Input(id='employee_num', disabled=True)
            )
        ],
            row=True
        )

        admin_status = dbc.FormGroup([
            dbc.Label('Admin Status:', width=4),
            dbc.Col(
                dbc.RadioItems(
                    id='admin_radio',
                    options=[
                        {'label': 'Yes', 'value': True},
                        {'label': 'No', 'value': False}
                    ]
                )
            ),
            dbc.Button('Save',
                       id='save_admin',
                       n_clicks=0,
                       size='md',
                       color='secondary',
                       disabled=True)
        ],
            row=True
        )

        return dbc.Form(id='admin-editor', children=[employee_select, employee_number, admin_status])


# endregion


# region Load employee
@app.callback([Output('employee_list', 'value'),
               Output('employee_num', 'value'),
               Output('admin_radio', 'value'),
               Output('save_admin', 'color'),
               Output('save_admin', 'disabled')],
              [Input('user_list', 'value')])
def load_employee(selection):
    if selection is None:
        return '', '', '', 'secondary', True
    data = CUSTOM_SQL.get_rows(EmployeeData, EmployeeData.employee_number_number == selection)[0]
    return f'{data.name_last}, {data.name_first}', selection, data.is_admin, 'success', False


# endregion


# region Save admin
@app.callback([Output('admin_save_toast', 'children'),
               Output('admin_save_toast', 'color'),
               Output('admin_save_toast', 'is_open')],
              [Input('save_admin', 'n_clicks')],
              [State('user_list', 'value'),
               State('admin_radio', 'value')])
def save_admin(save_click, selection, radio):
    if not save_click:
        raise PreventUpdate
    else:
        data = CUSTOM_SQL.get_rows(EmployeeData, EmployeeData.employee_number_number == selection)[0]
        if data.is_admin == radio:
            return 'Admin status not changed, nothing updated', 'danger', True
        else:
            app.logger.info(f'INFO :: Admin status for {data.name_last}, {data.name_first} has been updated to {radio}')
            CUSTOM_SQL.update_employee(selection, is_admin=radio)
            return 'Admin status updated', 'success', True


# endregion
# endregion


# region Employee Page callbacks
# region Employee editor data loading callback
@app.callback([Output('first-name', 'value'),
               Output('last-name', 'value'),
               Output('employee-number', 'value'),
               Output('employee-number', 'disabled'),
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
              [State('function', 'options')])
def load_employee_data(row, row_idx, func_op):
    """
    This loads selected employee data into the edit fields
    :param row: DataFrame
    :param row_idx: int
    :param func_op: []
    """
    if len(row_idx) > 0:
        quick_close_disabled = False
        save_button_disabled = False
        f_name = row[row_idx[0]]['name_first']
        l_name = row[row_idx[0]]['name_last']
        emp_num = row[row_idx[0]]['employee_number']
        job_code = row[row_idx[0]]['job_code']
        level = row[row_idx[0]]['level']
        pgms = []

        employee = CUSTOM_SQL.get_rows(EmployeeData, EmployeeData.employee_number_number == emp_num)
        for pgm in employee[0].employee_number.employee_pgm_assoc:
            pgms.append(CUSTOM_SQL.get_rows(Program, Program.name == pgm.employee_program)[0].id)

        try:
            func = [f for f in func_op if row[row_idx[0]]['function'] == f['label']][0]['value']
        except IndexError:
            func = None

        try:
            # pgm = [f for f in pgm_op if row[row_idx[0]]['programs'] == f['label']][0]['value']
            pgm = pgms
        except IndexError:
            pgm = None

        start = row[row_idx[0]]['date_start']
        end = row[row_idx[0]]['date_end']

        return f_name, l_name, emp_num, True, job_code, level, func, pgm, start, end, quick_close_disabled, \
               save_button_disabled
    else:
        return '', '', False, '', '', '', 0, 0, None, None, True, True


# endregion


# region Employee data table and editor button functions callback
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
def employee_editor_buttons(search_click, search_clear, new, save, close, clear, table_data, row_idx, search_text,
                            first_name, last_name, employee_number, job_code, level, func, pgm, start_date, end_date,
                            data):
    new = 0 if new is None else new
    save = 0 if save is None else save
    close = 0 if close is None else close
    clear = 0 if clear is None else clear
    search_click = 0 if search_click is None else search_click
    search_clear = 0 if search_clear is None else search_clear
    data_refresh = False
    cells = []
    data_set = table_data
    multi = False

    if row_idx and search_text == '':
        if func != (0 or None):
            func = CUSTOM_SQL.get_rows(Functions, Functions.id == func)[0].function

    editor_fields = [first_name,
                     last_name,
                     job_code,
                     level,
                     func,
                     pgm,
                     start_date,
                     end_date]

    # https://community.plot.ly/t/input-two-or-more-button-how-to-tell-which-button-is-pressed/5788/29
    # Search was clicked
    if all(search_click > x for x in (search_clear, new, save, close, clear)):
        if search_text is None:
            return row_idx, [], data, search_text
        queries = [q.strip() for q in search_text.split(',')]
        data_set = []
        if len(queries) > 1:
            multi = True
        for q in queries:
            data_set.append(CUSTOM_SQL.query_rows(q))
        row_idx = []
    # Search clear was clicked
    elif all(search_clear > x for x in (search_click, new, save, close, clear)):
        data_refresh = True
        row_idx = []
        search_text = ''
    # New was clicked
    elif all(new > x for x in (search_click, search_clear, save, close, clear)):
        if first_name is '' or last_name is '' or not isinstance(employee_number, int) \
                or job_code is '' or start_date is '':
            pass
        CUSTOM_SQL.add_employee(first_name=first_name, last_name=last_name, employee_number=employee_number,
                                job_code=job_code, level=level, func=func, pgms=pgm, start_date=start_date,
                                end_date=end_date)
        app.logger.info(
            f'INFO :: The user {data["login_user"]} added a new employee using the following information: first_name:'
            f'{first_name}, last_name:{last_name}, employee_number:{employee_number}, job_code:{job_code}, '
            f'level:{level}, function:{func}, program:{pgm}, start_date:{start_date}, end_date:{end_date}')
        data_refresh = True
    # Save was clicked
    elif all(save > x for x in (search_click, search_clear, new, close, clear)):
        updates_exist = False
        updated_indices = ''
        update_args = {}

        for i in range(len(data_fields)):
            if table_data[row_idx[0]][data_fields[i]] != editor_fields[i]:
                if i == 4:
                    # The function entered has changed
                    f = CUSTOM_SQL.get_rows(Functions, Functions.id == editor_fields[i])[0].function
                    if not table_data[row_idx[0]][data_fields[i]] == f:
                        updates_exist = True
                        update_args[data_fields[i]] = f
                        updated_indices += f', {data_fields[i]}: {table_data[row_idx[0]][data_fields[i]]} >> {f}'
                elif i == 5:
                    # The program(s) entered have changed
                    if len(editor_fields[i]) > 0 \
                            or len(table_data[row_idx[0]][data_fields[i]]) != len(editor_fields[i]) \
                            or (len(table_data[row_idx[0]][data_fields[i]]) > 0 and len(editor_fields[i]) == 0):
                        if len(editor_fields[i]) > 0:
                            for s in editor_fields[i]:
                                p = CUSTOM_SQL.get_rows(Program, Program.id == s)[0].name
                                if p not in table_data[row_idx[0]][data_fields[i]]:
                                    updates_exist = True
                                    update_args[data_fields[i]] = p
                        else:
                            updates_exist = True
                            update_args[data_fields[i]] = ''
                else:
                    # One of the other fields has changed
                    updates_exist = True
                    update_args[data_fields[i]] = editor_fields[i]
                    updated_indices += f', {data_fields[i]}: {table_data[row_idx[0]][data_fields[i]]} '
                    f'>> {editor_fields[i]}'
        if updates_exist:
            CUSTOM_SQL.update_employee(table_data[row_idx[0]]['employee_number'], **update_args)
            app.logger.info(
                f'INFO :: The user {data["login_user"]} updated the employee record for '
                f'{table_data[row_idx[0]]["name_first"]} {table_data[row_idx[0]]["name_last"]} with the following '
                f'information{updated_indices}')
            data_set = CUSTOM_SQL.query_rows(search_text)
    # Close was clicked
    elif all(close > x for x in (search_click, search_clear, new, save, clear)):
        data_refresh = True
        # print('close clicked: duplicating selected database entry, closing the original and loading the duplicate')
        # TODO: Prompt the user for a date to close the selected entry
        # TODO: Create a new entry with the selected entry data, replace the start
        # date with the selected close date and clear the close date
    # Clear was clicked
    elif all(clear > x for x in (search_click, search_clear, new, save, close)):
        data_refresh = True
        row_idx = []
        cells = []
        search_text = ''
    # Nothing was clicked
    else:
        data_refresh = True

    if data_refresh:
        data_set = CUSTOM_SQL.get_rows(EmployeeData)
        search_text = ''

    if multi:
        emp_ds = []
        for i in data_set:
            if len(i) > 1:
                for j in i:
                    emp_ds.append(j)
            elif len(i) == 0:
                pass
            else:
                emp_ds.append(i[0])
        emp_ds = CUSTOM_SQL.remove_duplicates(emp_ds)
    else:
        emp_ds = data_set

    if len(emp_ds) > 1:
        results = emp_ds
    else:
        results = emp_ds[0]

    data = [{'name_first': i.name_first,
             'name_last': i.name_last,
             'employee_number': i.employee_number_number,
             'job_code': i.job_code,
             'job_title': i.job_title,
             'level': i.level,
             'function': CUSTOM_SQL.get_rows(class_name=EmployeeFunctionLink,
                                             filter_text=EmployeeFunctionLink.employee_number ==
                                                         i.employee_number_number)[0].employee_function
             if len(CUSTOM_SQL.get_rows(class_name=EmployeeFunctionLink,
                                        filter_text=EmployeeFunctionLink.employee_number ==
                                                    i.employee_number_number)) > 0 else '',
             'programs': ', '.join([p.employee_program for p in
                                    CUSTOM_SQL.get_rows(class_name=EmployeeProgramLink,
                                                        filter_text=EmployeeProgramLink.employee_number ==
                                                                    i.employee_number_number)])
             if len(CUSTOM_SQL.get_rows(class_name=EmployeeProgramLink,
                                        filter_text=EmployeeProgramLink.employee_number ==
                                                    i.employee_number_number)) > 0 else '',
             'date_start': i.date_start,
             'date_end': i.date_end if i.date_end is not None else None} for i in results]
    return row_idx, cells, data, search_text


# endregion


# region Add new employee callback
@app.callback([Output('new-employee', 'disabled')],
              [Input('first-name', 'value'),
               Input('last-name', 'value'),
               Input('employee-number', 'value'),
               Input('job-code', 'value'),
               Input('start-date', 'date')])
def add_employee_button_state(first_name, last_name, employee_number, job_code, start_date):
    if first_name is '' or last_name is '' or not isinstance(employee_number, int) \
            or job_code is '' or start_date is '':
        return [True]
    return [False]


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
# endregion


# region Program Page callbacks
# region Upload new resource sheets
@app.callback(Output('programs-data-upload', 'children'),
              [Input('resource-worksheet-upload', 'contents'),
               Input('resource-worksheet-upload', 'filename')],
              [State('session-store', 'data')])
def update_programs_output(list_of_contents, list_of_names, session_data):
    if list_of_contents is not None:
        [parse_contents(c, n, session_data) for c, n in zip(list_of_contents, list_of_names)]

        return [dbc.ListGroupItem(file, style={'padding': '0 1rem'}) for file in list_of_names]


# endregion


# region Programs page filter tools
@app.callback(Output('programs-page-container', 'children'),
              [Input('page-content', 'value')],
              [State('session-store', 'data')])
def programs_page_content(value, data):
    charges = [{'label': charge[0], 'value': charge[0]} for charge in
               sorted(CUSTOM_SQL.get_rows(ResourceUsage.charge_number, distinct=True))]
    years = [{'label': year[0], 'value': year[0]} for year in
             sorted(CUSTOM_SQL.get_rows(ResourceUsage.year, distinct=True))]
    months = [{'label': month[0], 'value': month[0]} for month in
              sorted(CUSTOM_SQL.get_rows(ResourceUsage.month, distinct=True))]
    months = sorted(months, key=lambda i: time.strptime(i['value'], '%b-%y'))
    functions = [{'label': f.function, 'value': f.function} for f in
                 sorted(CUSTOM_SQL.get_rows(Functions), key=lambda k: k.function) if
                 f.finance_function is not None]

    if data is None or data['isadmin'] == False:
        tabs = [dcc.Tab(label='Program Resource Table', value='programs-table'),
                dcc.Tab(label='Program Resource Chart', value='programs-chart')]
    elif data['isadmin']:
        tabs = [dcc.Tab(label='Program Resource Table', value='programs-table'),
                dcc.Tab(label='Program Resource Chart', value='programs-chart'),
                dcc.Tab(label='Admin Controls', value='program-admin-controls')]

    layout = [dbc.Row(
        # TODO: look into maybe dynamically updating the filters based on other selections
        dbc.Col(id='programs-page-filter-options',
                children=[
                    dbc.Row([
                        dbc.Col([
                            html.Label('Charge #:'),
                            dcc.Dropdown(options=charges,
                                         id='charge_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Period:'),
                            dcc.Dropdown(options=[{'label': i, 'value': i} for i in range(1, 13)],
                                         id='period_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Sub-Pd:'),
                            dcc.Dropdown(options=[{'label': i, 'value': i} for i in range(1, 6)],
                                         id='sub_pd_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Quarter:'),
                            dcc.Dropdown(options=[{'label': i, 'value': i} for i in range(1, 5)],
                                         id='quarter_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Year:'),
                            dcc.Dropdown(options=years,
                                         id='year_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Month:'),
                            dcc.Dropdown(options=months,
                                         id='month_dd',
                                         multi=False)
                        ],
                            width='auto',
                        ),
                        dbc.Col([
                            html.Label('Function:'),
                            dcc.Dropdown(options=functions,
                                         id='function_dd',
                                         multi=False,
                                         optionHeight=30)
                        ],
                            width='auto',
                        )
                    ],
                        className='programs-page-filters'
                    )],
                align='start')
    ),
        html.Hr(),
        dbc.Row(
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        dbc.Button('Clear Filters',
                                   id='clear_programs_filters'),
                        width='auto'),
                    dbc.Col(
                        dbc.Button('Submit',
                                   id='submit_programs'),
                        width='auto')
                ],
                    justify='end',
                    className='programs-page-buttons'
                ),
                align='start',
                className='ml-auto'),
            style={'margin-bottom': '15px'}
        ),
        html.Div([
            dcc.Tabs(
                id='programs-tabs',
                value='programs-table',
                children=tabs,
                colors={
                    'border': 'white',
                    'primary': 'gold',
                    'background': 'cornsilk'
                },
                parent_style=card_style
            ),
            html.Div(children=[
                dcc.Loading(id='program-tabs-content',
                            type='cube')
            ])
        ])
    ]

    return layout


# endregion


# region Clear programs page filters
@app.callback([Output('charge_dd', 'value'),
               Output('period_dd', 'value'),
               Output('sub_pd_dd', 'value'),
               Output('year_dd', 'value'),
               Output('month_dd', 'value'),
               Output('quarter_dd', 'value'),
               Output('function_dd', 'value')],
              [Input('clear_programs_filters', 'n_clicks')])
def clear_programs_filters(clear):
    if not clear:
        raise PreventUpdate
    elif clear:
        return ['', '', '', '', '', '', '']


# endregion


# region Program tabs
@app.callback(Output('program-tabs-content', 'children'),
              [Input('url', 'pathname'),
               Input('programs-tabs', 'value'),
               Input('submit_programs', 'n_clicks')],
              [State('charge_dd', 'value'),
               State('period_dd', 'value'),
               State('sub_pd_dd', 'value'),
               State('year_dd', 'value'),
               State('month_dd', 'value'),
               State('quarter_dd', 'value'),
               State('function_dd', 'value')])
def program_data_loading(page, tab, search, chg, period, sub, yr, month, qtr, func):
    time.sleep(1)
    date_range = [date.today() + relativedelta(months=i) for i in range(-3, 13)]
    parsed_data = [{'function': f.function} for f in sorted(CUSTOM_SQL.get_rows(Functions), key=lambda k: k.function)
                   if f.finance_function is not None]

    if search:
        params = [chg, period, sub, yr, month, qtr, func]
        results = []
        if any(params):
            args = {}
            if chg is not None:
                args.update({'charge_number': chg})
            if period is not None:
                args.update({'period': period})
            if sub is not None:
                args.update({'sub_period': sub})
            if yr is not None:
                args.update({'year': yr})
            if month is not None:
                args.update({'month': month})
            if qtr is not None:
                args.update({'quarter': qtr})
            if func is not None:
                args.update({'function_name': func})

            results.extend(CUSTOM_SQL.get_rows(ResourceUsage, args))
        else:
            results = CUSTOM_SQL.get_rows(ResourceUsage)

        if len(results) == 0:
            parsed_data = [{'No Results': 'no_results'}]
            columns = [{'name': 'No Results', 'id': 'no_results'}]
        else:
            cols = []
            for m in results:
                if m.month not in cols:
                    cols.append(m.month)

            data = pd.DataFrame.from_records([s.to_dict() for s in results])

            tempcsv = StringIO(data.pivot_table(values='hours', index='function', columns='month', aggfunc='sum').
                               to_csv())
            parsed_data = pd.read_csv(tempcsv).to_dict('rows')
            columns = [{'name': 'Function', 'id': 'function'}]
            [columns.append({'name': m, 'id': m}) for m in cols]
    else:
        columns = [{'name': 'Function', 'id': 'function'}]
        [columns.append({'name': d.strftime('%b-%y'), 'id': d.strftime('%b-%y')}) for d in date_range]

    if tab == 'programs-table':
        content = dt.DataTable(
            id='programs',
            data=parsed_data,
            columns=columns,
            fill_width=False,
            style_header={
                'fontWeight': 'bold',
                'backgroundColor': 'rgb(230, 230 ,230)',
                'textAlign': 'center'
            },
            style_cell={
                'height': 'auto',
                'minWidth': '50px',
                'maxWidth': '50px',
                'whiteSpace': 'normal'
            },
            style_data={
                'whiteSpace': 'normal'
            },
            style_table={
                'overflowX': 'scroll'
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'},
                 'backgroundColor': 'rgb(221, 235, 247)'},
                {'if': {'column_id': 'function'},
                 'minWidth': '225px',
                 'fontSize': '14px',
                 'fontWeight': 'bold'}
            ]
        )
        return content
    elif tab == 'programs-chart':
        try:
            parsed_data = data.pivot_table(values='hours', index='function', columns='month', aggfunc='sum')
            months = [date.strftime(date(d[0], d[1], d[2]), '%b-%y') for d in sorted([time.strptime(m, '%b-%y')
                                                                                      for m in parsed_data.columns])]
            func_list = [f for f in parsed_data.reset_index()['function']]

            fig = go.Figure()
            for func in func_list:
                fig.add_trace(go.Bar(x=months,
                                     y=list(parsed_data.to_dict('index')[func].values()),
                                     name=func))

            fig.update_layout(
                title='Resource Utilization by Function',
                yaxis=dict(title='Hours',
                           titlefont_size=16,
                           tickfont_size=14),
                legend_title='<b>Functions</b>',
                # legend=dict(x=0,
                #             y=1.0,
                #             bgcolor='rgba(255, 255, 255, 0)',
                #             bordercolor='rgba(255, 255, 255, 0)'),
                barmode='group',
                bargap=0.15,  # gap between bars of adjacent location coordinates
                bargroupgap=0.1,  # gap between bars of the same location coordinate
            )

        except NameError:
            content = html.H6('No Data Loaded',
                              style={
                                  'width': '100%',
                                  'text-align': 'center',
                                  'font-size': '48px',
                                  'padding-top': '50px'})
            return content

        content = dcc.Graph(figure=fig,
                            style={'height': '65vh'})

        return content
    elif tab == 'program-admin-controls':
        content = html.Div([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.H5('Load existing data'),
                        html.Div(className='sidenav',
                                 children=[
                                     dcc.Dropdown(id='pgm-data-type-list',
                                                  options=[
                                                      {'label': 'Upload Data', 'value': 'type_upload'},
                                                      {'label': 'Charge Numbers', 'value': 'type_chg'},
                                                      {'label': 'Projects', 'value': 'type_proj'},
                                                      {'label': 'Major Programs', 'value': 'type_prog'},
                                                      {'label': 'Functions', 'value': 'type_func'}
                                                  ],
                                                  style={'width': '100%'},
                                                  clearable=False,
                                                  value='type_upload'),
                                     dbc.Checkbox(id='new_item_cb'),
                                     dbc.Label('Add New?'),
                                     html.Br(),
                                     dcc.Dropdown(id='pgm-data-list-items',
                                                  style={'width': '100%'})
                                 ]),
                    ],
                        width=3,
                        style={
                            'border-right': '1px solid gray',
                            'padding': '0px 15px 0px 0px'
                        }
                    ),
                    dbc.Col([
                        html.Div(id='editor-container')
                    ],
                        style={
                            'border-right': '1px solid gray'
                        }),

                ],
                    style={
                        'padding': '10px 5px'
                    })
            ])
        ])

        return content


# endregion


# region list item selection
@app.callback([Output('pgm-data-list-items', 'options'),
               Output('editor-container', 'children'),
               Output('pgm-data-list-items', 'style')],
              [Input('pgm-data-type-list', 'value'),
               Input('pgm-data-list-items', 'value'),
               Input('new_item_cb', 'checked')])
def load_test(type, selection, new_item):
    items_dd_options = []
    layout = [html.H5('Select an option or Add New from the left column to load data here.')]
    items_dd_display = {'visibility': 'visible'}

    if type == 'type_upload':
        layout = dbc.Col([
            dcc.Upload(
                id='resource-worksheet-upload',
                children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                style={'width': '100%',
                       'height': '60px',
                       'line-height': '60px',
                       'border-width': '1px',
                       'border-style': 'dashed',
                       'border-radius': '5px',
                       'textAlign': 'center',
                       'margin': '10px'},
                # Allow multiple files to be uploaded
                multiple=True),
            html.Label('Uploading workbooks will fail if the charge number does not exist yet:',
                       style={
                           'margin-bottom': '0px',
                           'fontWeight': 'bold'
                       }),
            html.Label('Recently Uploaded:',
                       style={
                           'margin-bottom': '0px',
                           'fontWeight': 'bold'
                       }),
            dcc.Loading(
                dbc.ListGroup(id='programs-data-upload',
                              children=[],
                              style={'max-height': '350px',
                                     'overflowY': 'scroll'})
            )
        ],
            className='ml-auto',
            align='start')
        items_dd_display = {'visibility': 'hidden'}
    elif type == 'type_chg':
        charges = CUSTOM_SQL.get_rows(ChargeNumber, ChargeNumber.charge_number != 'Null', distinct=True)
        items_dd_options = [{'label': c.charge_number, 'value': c.id} for c in
                            sorted(charges, key=lambda c: c.charge_number)]
    elif type == 'type_func':
        funcs = CUSTOM_SQL.get_rows(Functions, Functions.function != 'Null', distinct=True)
        items_dd_options = [{'label': f.function, 'value': f.id} for f in sorted(funcs, key=lambda f: f.function)]
    elif type == 'type_prog':
        maj_pgms = CUSTOM_SQL.get_rows(Program, Program.name != 'Null', distinct=True)
        items_dd_options = [{'label': m.name, 'value': m.id} for m in sorted(maj_pgms, key=lambda m: m.name)]
    elif type == 'type_proj':
        projs = CUSTOM_SQL.get_rows(ProjectData, distinct=True)
        items_dd_options = [{'label': p.name, 'value': p.id} for p in sorted(projs, key=lambda p: p.name)]

    if selection is None and new_item is False:
        return items_dd_options, layout, items_dd_display
    else:
        if new_item:
            items_dd_display = {'visibility': 'hidden'}

        if type == 'type_chg':  # Charge code type is selected
            if not new_item:
                if selection is not None:
                    head = 'Edit Charge Code'
                    try:
                        charge = CUSTOM_SQL.get_rows(ChargeNumber, ChargeNumber.id == selection)[0]
                        if not isinstance(charge, ChargeNumber):
                            return items_dd_options, layout, items_dd_display
                    except IndexError:
                        return items_dd_options, layout, items_dd_display
                    chg = charge.charge_number
                    btn = [update_btn,
                           delete_btn,
                           html.Label(id='update-status'),
                           html.Label(id='delete-status'),
                           dcc.ConfirmDialog(id='delete_confirm')]
                else:
                    head = 'Create Charge Code'
                    chg = ''
                    btn = []
            else:
                head = 'Create Charge Code'
                chg, prj, pgm, tp, st, ed = '', '', '', '', '', ''
                btn = [add_btn,
                       html.Label(id='add-status')]

            layout = [dbc.Row([
                dbc.Col(html.H5(head)),
                dbc.Col(btn, width=6)]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Charge Number:'),
                            dbc.Input(type='text',
                                      id='charge_num_input',
                                      value=chg)
                        ])
                    ],
                        width=6),
                ])
            ]
        elif type == 'type_func':  # Function type is selected
            if not new_item:
                if selection is not None:
                    head = 'Edit Function'
                    try:
                        func = CUSTOM_SQL.get_rows(Functions, Functions.id == selection)[0]
                        if not isinstance(func, Functions):
                            return items_dd_options, layout, items_dd_display
                    except IndexError:
                        return items_dd_options, layout, items_dd_display
                    func_name = func.function
                    fin_func_name = func.finance_function if func.finance_function is not None \
                        else '' if not new_item else ''
                    btn = [update_btn,
                           delete_btn,
                           html.Label(id='update-status'),
                           html.Label(id='delete-status'),
                           dcc.ConfirmDialog(id='delete_confirm')]
                else:
                    head = 'Create Function'
                    func_name = ''
                    fin_func_name = ''
                    btn = []
            else:
                head = 'Create Function'
                func_name = ''
                fin_func_name = ''
                btn = [add_btn,
                       html.Label(id='add-status')]

            layout = [dbc.Row([
                dbc.Col(html.H5(head)),
                dbc.Col(btn, width=6)]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Functions:'),
                            dbc.Input(type='text',
                                      id='func_name_entry',
                                      value=func_name),
                            dbc.Tooltip(
                                'The name entered here is the general name for the given function. '
                                'This name just corresponds to a given finance function and can be left blank '
                                'if desired. The name entered here will not have an impact on data retrieved or '
                                'parsed from resource workbooks.',
                                target='func_name_entry')
                        ])
                    ],
                        width=12
                    )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Finance Function:'),
                            dbc.Input(type='text',
                                      id='fin_func_name_entry',
                                      value=fin_func_name),
                            dbc.Tooltip(
                                'The name entered here should reflect the finance function names as they are '
                                'listed in the resource worksheets. If the names don\'t match the data being '
                                'parsed from the workbooks could be incorrect or may not be retrieved at all.',
                                target='fin_func_name_entry')
                        ])
                    ],
                        width=12
                    )
                ])
            ]
        elif type == 'type_proj':  # Project type is selected
            maj_pgms = CUSTOM_SQL.get_rows(Program.name, Program.name != 'Null', distinct=True)
            charges = [{'label': c.charge_number, 'value': c.id} for c in CUSTOM_SQL.get_rows(ChargeNumber)]
            if not new_item:
                if selection is not None:
                    head = 'Edit Project Data'
                    try:
                        func = CUSTOM_SQL.get_rows(ProjectData, ProjectData.id == selection)[0]
                        if not isinstance(func, ProjectData):
                            return items_dd_options, layout, items_dd_display
                    except IndexError:
                        return items_dd_options, layout, items_dd_display
                    try:
                        chg = func.charge_number.id
                    except AttributeError:
                        chg = ''
                    prj = func.name
                    prog_link = CUSTOM_SQL.get_rows(ProgramProjectLink, ProgramProjectLink.project_name == prj)[0]
                    pgm = prog_link.program_name
                    tp = func.program_type
                    st = func.date_start
                    ed = func.date_end
                    btn = [update_btn,
                           delete_btn,
                           html.Label(id='update-status'),
                           html.Label(id='delete-status'),
                           dcc.ConfirmDialog(id='delete_confirm')]
                else:
                    head = 'Create Project'
                    chg, prj, pgm, tp, st, ed = '', '', '', '', '', ''
                    btn = []
            else:
                head = 'Create Project'
                chg, prj, pgm, tp, st, ed = '', '', '', '', date.today(), None
                btn = [add_btn,
                       html.Label(id='add-status')]

            layout = [dbc.Row([
                dbc.Col(html.H5(head)),
                dbc.Col(btn, width=6)]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Charge Number:'),
                            dcc.Dropdown(id='charge_num_dd',
                                         options=charges,
                                         value=chg)
                        ])
                    ],
                        width=6
                    )
                ]),
                dbc.Row(
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Project Name:'),
                            dbc.Input(type='text',
                                      id='project_name_input',
                                      value=prj)
                        ]),
                        dbc.FormGroup([
                            dbc.Label('Major Program:'),
                            dcc.Dropdown(id='major_pgm_dd',
                                         options=[{'label': p[0], 'value': p[0]} for p in maj_pgms if
                                                  p[0] is not None],
                                         multi=False,
                                         value=pgm)
                        ]),
                        dbc.FormGroup([
                            dbc.Label('Program Type:'),
                            dcc.RadioItems(id='pgm_type',
                                           options=[{'label': 'Firm', 'value': 'Firm'},
                                                    {'label': 'Potential Follow-On',
                                                     'value': 'Potential Follow-On'},
                                                    {'label': 'Potential New', 'value': 'Potential New'}]
                                           ,
                                           labelStyle={'display': 'block',
                                                       'padding': '0px'},
                                           value=tp)
                        ]),
                        dbc.FormGroup([
                            dbc.Row([
                                dbc.Col(
                                    dbc.Label('Start Date:'),
                                    width=6
                                ),
                                dbc.Col(
                                    dbc.Label('End Date:'),
                                    width=6
                                ),
                            ]),
                            dbc.Row([
                                dbc.Col(
                                    dcc.DatePickerSingle(id='proj_date_start',
                                                         with_portal=True,
                                                         className='required', placeholder='Start Date',
                                                         display_format='DD-MMM-YY',
                                                         clearable=True,
                                                         date=st,
                                                         style={'fontSize': '14px'}),
                                    width=6
                                ),
                                dbc.Col(
                                    dcc.DatePickerSingle(id='proj_date_end',
                                                         with_portal=True,
                                                         className='required', placeholder='End Date',
                                                         display_format='DD-MMM-YY',
                                                         clearable=True,
                                                         date=ed,
                                                         style={'fontSize': '14px'}),
                                    width=6
                                )
                            ])
                        ])
                    ])
                )
            ]
        elif type == 'type_prog':  # Major Program type is selected
            projects = CUSTOM_SQL.get_rows(ProjectData)
            employees = CUSTOM_SQL.get_rows(EmployeeData, filter_text=EmployeeData.date_end == None, distinct=True)
            if not new_item:
                if selection is not None:
                    head = 'Edit Major Program'
                    try:
                        func = CUSTOM_SQL.get_rows(Program, Program.id == selection)[0]
                        if not isinstance(func, Program):
                            return items_dd_options, layout, items_dd_display
                    except IndexError:
                        return items_dd_options, layout, items_dd_display
                    prog_name = func.name
                    comments = func.comments if func.comments is not None else '' if not new_item else ''
                    # Build the project items lists for the drop downs and list boxes
                    projs = CUSTOM_SQL.get_rows(ProgramProjectLink, ProgramProjectLink.program_name == func.name)
                    # TODO: See about optimizing this
                    l_p_dd = [{'label': x.name, 'value': f'{x.id}'} for x in projects if
                              x.name not in [p.project_name for p in projs]]
                    r_p_dd = [{'label': x.name, 'value': f'{x.id}'} for x in projects if
                              x.name in [p.project_name for p in projs]]
                    l_p_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in l_p_dd]
                    r_p_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in r_p_dd]

                    # Build the employee item lists for the drop downs and list boxes
                    emps = [i.number for i in func.employees]
                    # TODO: See about optimizing this
                    l_e_dd = [{'label': f'{x.name_last}, {x.name_first}', 'value': f'{x.employee_number_number}'}
                              for x in employees if x.employee_number_number not in emps]
                    r_e_dd = [{'label': f'{x.name_last}, {x.name_first}', 'value': f'{x.employee_number_number}'}
                              for x in employees if x.employee_number_number in emps]
                    l_e_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in l_e_dd]
                    r_e_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in r_e_dd]

                    btn = [update_btn,
                           delete_btn,
                           html.Label(id='update-status'),
                           html.Label(id='delete-status'),
                           dcc.ConfirmDialog(id='delete_confirm')]
                else:
                    head = 'Create Major Program'
                    prog_name = ''
                    comments = ''

                    # Build the project items lists for the drop downs and list boxes
                    l_p_dd = []
                    r_p_dd = []
                    l_p_list = []
                    r_p_list = []

                    # Build the employee item lists for the drop downs and list boxes
                    l_e_dd = []
                    r_e_dd = []
                    l_e_list = []
                    r_e_list = []
                    btn = []
            else:
                head = 'Create Major Program'
                prog_name = ''
                comments = ''

                # Build the project items lists for the drop downs and list boxes
                l_p_dd = [{'label': x.name, 'value': f'{x.id}'} for x in projects]
                r_p_dd = []
                l_p_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in l_p_dd]
                r_p_list = []

                # Build the employee item lists for the drop downs and list boxes
                l_e_dd = [{'label': f'{x.name_last}, {x.name_first}', 'value': f'{x.employee_number_number}'}
                          for x in employees]
                r_e_dd = []
                l_e_list = [html.Option(x['label'], id=f"{x['value']}", className='pgm-list-item') for x in l_e_dd]
                r_e_list = []
                btn = [add_btn,
                       html.Label(id='add-status')]

            layout = [dbc.Row([
                dbc.Col(html.H5(head)),
                dbc.Col(btn, width=6)]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Program Name:'),
                            dbc.Input(type='text',
                                      id='prog_name_entry',
                                      value=prog_name),
                            dbc.Tooltip(
                                'This is the name of the major program. (eg. SENTRY, VQ, S2GR)',
                                target='prog_name_entry')
                        ])
                    ],
                        width=5
                    ),
                    dbc.Col([
                        dbc.FormGroup([
                            dbc.Label('Program Comments:'),
                            dbc.Textarea(id='prog_comments_entry',
                                         value=comments),
                            dbc.Tooltip(
                                'Enter any program comments here, usually this is used to write out the full '
                                'program name since the name field is typically the commonly used name.',
                                target='prog_comments_entry')
                        ])
                    ],
                        width=6
                    )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            # dbc.Label('Projects:'),
                            dcc.Dropdown(id='pgm-proj-admin-dd-left',
                                         className='pgm-admin-dd',
                                         options=l_p_dd,
                                         multi=True),
                            html.Select(id='pgm-proj-admin-list-left',
                                        className='pgm-admin-list',
                                        children=l_p_list,
                                        disabled=True,
                                        size=6)])
                    ], className='pgm-admin-container',
                        width=5
                    ),
                    dbc.Col([
                        html.Div(id='buttons',
                                 children=[dbc.Row(dbc.Button('>', id='add-one-proj',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('>>', id='add-all-proj',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('<', id='remove-one-proj',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('<<', id='remove-all-proj',
                                                              className='pgm-admin-button'))]
                                 )
                    ], className='pgm-admin-button-container',
                    ),
                    dbc.Col([
                        dbc.FormGroup([
                            dcc.Dropdown(id='pgm-proj-admin-dd-right',
                                         className='pgm-admin-dd',
                                         options=r_p_dd,
                                         multi=True),
                            html.Select(id='pgm-proj-admin-list-right',
                                        className='pgm-admin-list',
                                        children=r_p_list,
                                        disabled=True,
                                        size=6)])
                    ], className='pgm-admin-container',
                        width=5
                    )
                ], id='pgm-admin-parent'),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            # dbc.Label('Projects:'),
                            dcc.Dropdown(id='pgm-emp-admin-dd-left',
                                         className='pgm-admin-dd',
                                         options=l_e_dd,
                                         multi=True),
                            html.Select(id='pgm-emp-admin-list-left',
                                        className='pgm-admin-list',
                                        children=l_e_list,
                                        disabled=True,
                                        size=6)])
                    ], className='pgm-admin-container',
                        width=5
                    ),
                    dbc.Col([
                        html.Div(id='buttons',
                                 children=[dbc.Row(dbc.Button('>', id='add-one-emp',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('>>', id='add-all-emp',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('<', id='remove-one-emp',
                                                              className='pgm-admin-button')),
                                           dbc.Row(dbc.Button('<<', id='remove-all-emp',
                                                              className='pgm-admin-button'))]
                                 )
                    ], className='pgm-admin-button-container',
                    ),
                    dbc.Col([
                        dbc.FormGroup([
                            dcc.Dropdown(id='pgm-emp-admin-dd-right',
                                         className='pgm-admin-dd',
                                         options=r_e_dd,
                                         multi=True),
                            html.Select(id='pgm-emp-admin-list-right',
                                        className='pgm-admin-list',
                                        children=r_e_list,
                                        disabled=True,
                                        size=6)])
                    ], className='pgm-admin-container',
                        width=5
                    )
                ], id='pgm-admin-parent')
            ]

    return items_dd_options, layout, items_dd_display


# endregion


def programs_listbox_item_movement(click, dd_opts, left_dd, left_list, list_opts, right_dd, right_list):
    if click == 'add_one':
        if len(left_dd) > 0:
            new_right_ids = [x['props']['id'] for x in right_list]
            new_right_ids += [x for x in left_dd if x not in new_right_ids]

            l_dd = [x for x in dd_opts if x['value'] not in new_right_ids]
            l_list = [html.Option(x['label'], id=f"{x['value']}") for x in l_dd]
            r_dd = [{'label': x['label'], 'value': x['value']} for x in dd_opts if f"{x['value']}" in new_right_ids]
            r_list = [html.Option(x.children, id=f"{x.id}") for x in list_opts if f'{x.id}' in new_right_ids]
            return l_dd, r_dd, l_list, r_list, [], []
        else:
            return left_dd, right_dd, left_list, right_list, [], []
    elif click == 'add_all':
        return [], dd_opts, [], list_opts, [], []
    elif click == 'rem_one':
        if len(right_dd) > 0:
            new_left_ids = [x['props']['id'] for x in left_list]
            new_left_ids += [x for x in right_dd if x not in new_left_ids]

            r_dd = [x for x in dd_opts if x['value'] not in new_left_ids]
            r_list = [html.Option(x['label'], id=f"{x['value']}") for x in r_dd]
            l_dd = [{'label': x['label'], 'value': x['value']} for x in dd_opts if f"{x['value']}" in new_left_ids]
            l_list = [html.Option(x.children, id=f"{x.id}") for x in list_opts if f'{x.id}' in new_left_ids]
            return l_dd, r_dd, l_list, r_list, [], []
        else:
            return left_dd, right_dd, left_list, right_list, [], []
    elif click == 'rem_all':
        return dd_opts, [], list_opts, [], [], []
    if click is None:
        return dd_opts, [], list_opts, [], [], []


# region program admin project list control
@app.callback([Output('pgm-proj-admin-dd-left', 'options'),
               Output('pgm-proj-admin-dd-right', 'options'),
               Output('pgm-proj-admin-list-left', 'children'),
               Output('pgm-proj-admin-list-right', 'children'),
               Output('pgm-proj-admin-dd-left', 'value'),
               Output('pgm-proj-admin-dd-right', 'value')],
              [Input('add-one-proj', 'n_clicks_timestamp'),
               Input('add-all-proj', 'n_clicks_timestamp'),
               Input('remove-one-proj', 'n_clicks_timestamp'),
               Input('remove-all-proj', 'n_clicks_timestamp')],
              [State('pgm-proj-admin-dd-left', 'value'),
               State('pgm-proj-admin-dd-right', 'value'),
               State('pgm-proj-admin-list-left', 'children'),
               State('pgm-proj-admin-list-right', 'children')])
def move_items(add_one, add_all, rem_one, rem_all, left_dd, right_dd, left_list, right_list):
    add_one = 0 if add_one is None else add_one
    add_all = 0 if add_all is None else add_all
    rem_one = 0 if rem_one is None else rem_one
    rem_all = 0 if rem_all is None else rem_all

    if all(add_one > x for x in (add_all, rem_one, rem_all)):
        click = 'add_one'
    elif all(add_all > x for x in (add_one, rem_one, rem_all)):
        click = 'add_all'
    elif all(rem_one > x for x in (add_one, add_all, rem_all)):
        click = 'rem_one'
    elif all(rem_all > x for x in (add_one, add_all, rem_one)):
        click = 'rem_all'
    else:
        click = None

    projects = CUSTOM_SQL.get_rows(ProjectData)

    dd_opts = [{'label': i.name, 'value': f'{i.id}'} for i in projects]

    list_opts = [html.Option(i.name, id=f'{i.id}') for i in projects]

    return programs_listbox_item_movement(click, dd_opts, left_dd, left_list, list_opts, right_dd, right_list)


# endregion


# region program admin employee list control
@app.callback([Output('pgm-emp-admin-dd-left', 'options'),
               Output('pgm-emp-admin-dd-right', 'options'),
               Output('pgm-emp-admin-list-left', 'children'),
               Output('pgm-emp-admin-list-right', 'children'),
               Output('pgm-emp-admin-dd-left', 'value'),
               Output('pgm-emp-admin-dd-right', 'value')],
              [Input('add-one-emp', 'n_clicks_timestamp'),
               Input('add-all-emp', 'n_clicks_timestamp'),
               Input('remove-one-emp', 'n_clicks_timestamp'),
               Input('remove-all-emp', 'n_clicks_timestamp')],
              [State('pgm-emp-admin-dd-left', 'value'),
               State('pgm-emp-admin-dd-right', 'value'),
               State('pgm-emp-admin-list-left', 'children'),
               State('pgm-emp-admin-list-right', 'children')])
def move_items(add_one, add_all, rem_one, rem_all, left_dd, right_dd, left_list, right_list):
    add_one = 0 if add_one is None else add_one
    add_all = 0 if add_all is None else add_all
    rem_one = 0 if rem_one is None else rem_one
    rem_all = 0 if rem_all is None else rem_all

    if all(add_one > x for x in (add_all, rem_one, rem_all)):
        click = 'add_one'
    elif all(add_all > x for x in (add_one, rem_one, rem_all)):
        click = 'add_all'
    elif all(rem_one > x for x in (add_one, add_all, rem_all)):
        click = 'rem_one'
    elif all(rem_all > x for x in (add_one, add_all, rem_one)):
        click = 'rem_all'
    else:
        click = None

    emps = CUSTOM_SQL.get_rows(EmployeeData, EmployeeData.date_end == None)

    dd_opts = [{'label': f'{i.name_last}, {i.name_first}', 'value': f'{i.employee_number_number}'}
               for i in emps]

    list_opts = [html.Option(f'{i.name_last}, {i.name_first}', id=f'{i.employee_number_number}')
                 for i in emps]

    return programs_listbox_item_movement(click, dd_opts, left_dd, left_list, list_opts, right_dd, right_list)


# endregion


# region update entry
@app.callback(Output('update-status', 'value'),
              [Input('update_entry', 'n_clicks')],
              [State('pgm-data-type-list', 'value'),
               State('pgm-data-list-items', 'value'),
               State('editor-container', 'children')])
def update_function(click, type_dd, selection, form_contents):
    if not click:
        raise PreventUpdate

    if type_dd == 'type_chg':
        chg = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['value']
        CUSTOM_SQL.update_charge_code(chg_id=selection, charge_code_entry=chg)
    elif type_dd == 'type_func':
        func = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props'][
            'value']
        fin_func = form_contents[2]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props'][
            'value']
        CUSTOM_SQL.update_function(func_id=selection, func_entry=func, fin_func_entry=fin_func)
    elif type_dd == 'type_proj':
        chg = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['value']
        proj = form_contents[2]['props']['children']['props']['children'][0]['props']['children'][1]['props']['value']
        pgm = form_contents[2]['props']['children']['props']['children'][1]['props']['children'][1]['props']['value']
        pgm_type = form_contents[2]['props']['children']['props']['children'][2]['props']['children'][1] \
            ['props']['value']
        start = form_contents[2]['props']['children']['props']['children'][3]['props']['children'][1] \
            ['props']['children'][0]['props']['children']['props']['date']
        start = date(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
        end = form_contents[2]['props']['children']['props']['children'][3]['props']['children'][1] \
            ['props']['children'][1]['props']['children']['props']['date']
        if end is not None:
            end = date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
        else:
            end = None

        CUSTOM_SQL.update_project_data(chg_id=chg,
                                       project_name=proj, major_program=pgm, program_type=pgm_type,
                                       project_date_start=start, project_date_end=end)
    elif type_dd == 'type_prog':
        # TODO: retrieve values from the programs fields and update that appropriate entry and link tables
        pgm_name = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1] \
            ['props']['value']
        pgm_comments = form_contents[1]['props']['children'][1]['props']['children'][0]['props']['children'][1] \
            ['props']['value']
        proj_lb = form_contents[2]['props']['children'][2]['props']['children'][0]['props']['children'][1] \
            ['props']['children']
        projs = [x['props']['id'] for x in proj_lb]
        emp_lb = form_contents[3]['props']['children'][2]['props']['children'][0]['props']['children'][1] \
            ['props']['children']
        emps = [x['props']['id'] for x in emp_lb]
        CUSTOM_SQL.update_program(prog_id=selection,
                                  program_name=pgm_name, program_comments=pgm_comments,
                                  projects=projs, employees=emps)


# endregion


# region add entry
@app.callback(Output('add-status', 'value'),
              [Input('add_entry', 'n_clicks')],
              [State('pgm-data-type-list', 'value'),
               State('editor-container', 'children')])
def add_function(click, type_dd, form_contents):
    if not click:
        raise PreventUpdate

    if type_dd == 'type_chg':
        chg = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['value']
        CUSTOM_SQL.add_charge_code(charge_number=chg)
    elif type_dd == 'type_func':
        func = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props'][
            'value']
        fin_func = form_contents[2]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props'][
            'value']
        CUSTOM_SQL.add_function(func_entry=func, fin_func_entry=fin_func)
    elif type_dd == 'type_proj':
        chg = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1]['props']['value']
        proj = form_contents[2]['props']['children']['props']['children'][0]['props']['children'][1]['props']['value']
        pgm = form_contents[2]['props']['children']['props']['children'][1]['props']['children'][1]['props']['value']
        pgm_type = form_contents[2]['props']['children']['props']['children'][2]['props']['children'][1] \
            ['props']['value']
        start = form_contents[2]['props']['children']['props']['children'][3]['props']['children'][1] \
            ['props']['children'][0]['props']['children']['props']['date']
        start = date(int(start.split('-')[0]), int(start.split('-')[1]), int(start.split('-')[2]))
        end = form_contents[2]['props']['children']['props']['children'][3]['props']['children'][1] \
            ['props']['children'][1]['props']['children']['props']['date']
        if end is not None:
            end = date(int(end.split('-')[0]), int(end.split('-')[1]), int(end.split('-')[2]))
        else:
            end = None

        CUSTOM_SQL.add_project_data(chg_id=chg, proj_name=proj, maj_prog=pgm, prog_type=pgm_type,
                                    date_start=start, date_end=end)
    elif type_dd == 'type_prog':
        pgm_name = form_contents[1]['props']['children'][0]['props']['children'][0]['props']['children'][1] \
            ['props']['value']
        pgm_comments = form_contents[1]['props']['children'][1]['props']['children'][0]['props']['children'][1] \
            ['props']['value']
        proj_lb = form_contents[2]['props']['children'][2]['props']['children'][0]['props']['children'][1] \
            ['props']['children']
        projs = [x['props']['children'] for x in proj_lb]
        emp_lb = form_contents[3]['props']['children'][2]['props']['children'][0]['props']['children'][1] \
            ['props']['children']
        emps = [x['props']['id'] for x in emp_lb]
        CUSTOM_SQL.add_program(prog_name=pgm_name, prog_comments=pgm_comments, projects=projs, employees=emps)
        pass


# endregion


# region delete confirm prompt
@app.callback([Output('delete_confirm', 'displayed'),
               Output('delete_confirm', 'message')],
              [Input('delete_entry', 'n_clicks')],
              [State('pgm-data-type-list', 'value'),
               State('pgm-data-list-items', 'value')])
def show_delete_confirmation(prompt, selected_type, selected_item):
    if not prompt:
        return False, ''
    if selected_type == 'type_chg':
        st = 'Charge Number'
        it = CUSTOM_SQL.get_rows(ChargeNumber.charge_number, ChargeNumber.id == selected_item)[0][0]
    elif selected_type == 'type_func':
        st = 'Function'
        it = CUSTOM_SQL.get_rows(Functions.function, Functions.id == selected_item)[0][0]
    elif selected_type == 'type_proj':
        st = 'Project'
        it = CUSTOM_SQL.get_rows(ProjectData.name, ProjectData.id == selected_item)[0][0]
    elif selected_type == 'type_prog':
        st = 'Program'
        it = CUSTOM_SQL.get_rows(Program.name, Program.id == selected_item)[0][0]
    message = f'Are you sure you want to delete the {st} "{it}"? This action cannot be undone!'
    return True, message


# endregion


# region delete item
@app.callback(Output('delete-status', 'displayed'),
              [Input('delete_confirm', 'submit_n_clicks')],
              [State('pgm-data-type-list', 'value'),
               State('pgm-data-list-items', 'value')])
def delete_item(confirmed, type_dd, selection):
    if confirmed:
        if type_dd == 'type_chg':
            CUSTOM_SQL.delete_charge_code(chg_id=selection)
        elif type_dd == 'type_func':
            CUSTOM_SQL.delete_function(func_id=selection)
        elif type_dd == 'type_proj':
            CUSTOM_SQL.delete_project_data(proj_id=selection)
        elif type_dd == 'type_prog':
            CUSTOM_SQL.delete_program(prog_id=selection)


# endregion
# endprogram


# region Capacity Page callbacks
# region Employee data table and editor button functions callback
@app.callback(Output('capacity-tabs-content', 'children'),
              [Input('capacity-tabs', 'value')])
def capacity_data_loading(tab):
    time.sleep(1)
    date_range = [date.today() + relativedelta(months=i) for i in range(-3, 13)]
    columns = [{'name': 'Functions', 'id': 'Functions'}]
    for i in range(16):
        columns.append({'name': (date_range[i]).strftime('%b-%y').upper(), 'id': (date_range[i]).strftime('%b-%y').
                       upper()})

    func_rows = [x.function for x in [f for f in CUSTOM_SQL.get_rows(Functions)] if x.finance_function is not None]
    func_rows.append('Totals')

    data = [func_rows]

    results = pd.DataFrame({columns[0]['name']: data[0]})

    # TODO: Update this method so that it returns an initial dataframe then iterate through months with that, this
    #  should speed it up substantially
    for i in range(len(date_range)):
        col = CUSTOM_SQL.get_counts(date_range[i]).values()
        data.append(col)
        results = results.join(pd.DataFrame({(date_range[i]).strftime('%b-%y').upper(): list(col)}))

    if tab == 'capacity-table':
        return dt.DataTable(
            id='capacity',
            columns=columns,
            data=results.to_dict('records'),
            style_as_list_view=True,
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bolder',
                'fontSize': '16px',
                'textAlign': 'center'
            },
            style_data={
                'textAlign': 'center',
                'fontSize': '14px',
                'fontWeight': 'bold',
                'height': 'auto',
                'width': 'auto'
            },
            style_data_conditional=[
                {'if': {'row_index': 'odd'},
                 'backgroundColor': 'rgb(248, 248, 248)'},
                {'if': {'row_index': len(func_rows) - 1},
                 'backgroundColor': 'rgb(175, 175, 175)',
                 'fontSize': '16px'},
                {'if': {'column_id': 'Functions'},
                 'textAlign': 'right',
                 'padding': '0px 15px 0px 0px',
                 'fontSize': '12px'}
            ],
            fixed_columns={'headers': True, 'data': 1},
            fixed_rows={'headers': True, 'data': 0}
        )
    elif tab == 'capacity-chart':
        # https://pbpython.com/plotly-dash-intro.html
        chart_data = []
        for i in range(len(func_rows) - 1):
            chart_data.append(go.Bar(x=date_range,
                                     y=list(results.loc[i]),
                                     name=results.loc[i][0]))
        return dcc.Graph(
            id='capacity-graph',
            figure={
                'data': chart_data,
                'layout':
                    go.Layout(
                        title='Employee Capacity',
                        barmode='group'
                    )
            },
            style={'height': '75vh'}
        )
# endregion
# endregion
