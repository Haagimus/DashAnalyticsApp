import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable

import assets.SQL as sql
from assets.models import Program, EmployeeData, Functions

employees = sql.get_rows(EmployeeData)


def employee_table(data):
    if data is not None and data['isadmin']:
        # This is the admin layout
        columns = [{'name': 'First Name', 'id': 'name_first', "hideable": True},
                   {'name': 'Last Name', 'id': 'name_last', "hideable": True},
                   {'name': 'Employee #', 'id': 'employee_number', "hideable": True},
                   {'name': 'Job Code', 'id': 'job_code', "hideable": True},
                   {'name': 'Job Title', 'id': 'job_title', "hideable": True},
                   {'name': 'Level', 'id': 'level', "hideable": True},
                   {'name': 'Assigned Function', 'id': 'function', "hideable": True},
                   {'name': 'Assigned Program(s)', 'id': 'programs', "hideable": True},
                   {'name': 'Start Date', 'id': 'date_start', "hideable": True},
                   {'name': 'End Date', 'id': 'date_end', "hideable": True}]
    else:
        columns = [{'name': 'First Name', 'id': 'name_first', "hideable": True},
                   {'name': 'Last Name', 'id': 'name_last', "hideable": True},
                   {'name': 'Employee #', 'id': 'employee_number', "hideable": True},
                   {'name': 'Job Code', 'id': 'job_code', "hideable": True},
                   {'name': 'Assigned Function', 'id': 'function', "hideable": True},
                   {'name': 'Assigned Program(s)', 'id': 'program', "hideable": True},
                   {'name': 'Start Date', 'id': 'date_start', "hideable": True}]
    table = DataTable(
        id='Employees',
        columns=columns,
        data=[],
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
        style_table={
            'overflowX': 'scroll',
            'border': 'solid 1px black'
        },
        row_selectable='single',
        selected_rows=[]
    )

    return table


def employee_page_layout(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}
    if data['isadmin']:
        display = [8, 109, 'grid']
    else:
        display = [12, 12, 'none']

    layout = dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.InputGroup([
                    dbc.Input(id='search', placeholder='search employees'),
                    dbc.InputGroupAddon([
                        dbc.Button('Clear', id='clear-search', n_clicks_timestamp=0),
                        dbc.Button('Search', id='search-button', n_clicks_timestamp=0)],
                        addon_type='append'
                    )
                ])
            ),
            dbc.Row(
                html.Div(
                    dcc.Loading(id='employees-loading',
                                children=[
                                    html.Div(employee_table(data),
                                             id='employee-container',
                                             style={'width': 'auto'})
                                ],
                                type='default'
                                ),
                    style={'width': '100%',
                           'padding-top': '10px'}
                ),
                justify='between'
            )
        ],
            md=display[0],
            lg=display[1]),
        dbc.Col([
            html.H3('Employee Editor:'),
            dbc.Row(
                dbc.Col([
                    dbc.Label('First Name: *'),
                    dbc.Input(id='first-name',
                              type='text',
                              className='required',
                              placeholder='First Name')])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Last Name: *'),
                    dbc.Input(id='last-name',
                              type='text',
                              className='required',
                              placeholder='Last Name')])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Employee Number: *'),
                    dbc.Input(id='employee-number',
                              type='number',
                              className='required',
                              placeholder='Employee Number')])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Job Code: *'),
                    dbc.Input(id='job-code',
                              type='text',
                              className='required',
                              placeholder='Job Code')])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Assigned Function'),
                    dcc.Dropdown(id='function',
                                 options=[{'label': i.function, 'value': i.id}
                                          for i in sql.get_rows(Functions)],
                                 placeholder='Select Function',
                                 searchable=True)])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Assigned Program(s)'),
                    dcc.Dropdown(id='program-name',
                                 options=[{'label': i.name, 'value': i.id}
                                          for i in sql.get_rows(Program)],
                                 placeholder='Select Program(s)',
                                 multi=True,
                                 searchable=True)])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('Start Date'),
                    dcc.DatePickerSingle(id='start-date',
                                         with_portal=True,
                                         placeholder='Start Date',
                                         display_format='DD-MMM-YY')])),
            dbc.Row(
                dbc.Col([
                    dbc.Label('End Date'),
                    dcc.DatePickerSingle(id='end-date',
                                         with_portal=True,
                                         placeholder='End Date',
                                         display_format='DD-MMM-YY')])),
            dbc.Row(id='edit-employee-buttons',
                    children=[
                        dbc.Col(
                            dbc.Button('Load Selected',
                                       id='load-employee',
                                       n_clicks=0)),
                        dbc.Col(
                            dbc.Button('Save',
                                       id='save-employee',
                                       n_clicks=0,
                                       style={'width': 'inherit',
                                              'height': '100%'}))],
                    style={'margin-top': '10px'})
        ],
            id='employee-editor',
            md=4,
            lg=2,
            style={'max-width': '300px',
                   'display': display[2],
                   'height': 'calc(1vh - 150px)'})
    ])

    return layout
