import datetime as dt

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
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
                   # {'name': 'Job Title', 'id': 'job_title', "hideable": True},
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
                   {'name': 'Assigned Program(s)', 'id': 'programs', "hideable": True},
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


def employee_editor():
    editor = [
        dbc.Row([
            dbc.Col(
                html.A('x',
                       className='close-editor',
                       id='close-employee-editor',
                       n_clicks_timestamp=0),
                width=2
            ),
            dbc.Col(
                html.H4('Employee Editor'),
                width={'size': 9, 'offset': 1}
            )]
        ),
        dbc.Row(
            dbc.Col([
                dbc.Label('First Name: (required)'),
                dbc.Input(id='first-name',
                          type='text',
                          className='required',
                          placeholder='First Name')])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Last Name: (required)'),
                dbc.Input(id='last-name',
                          type='text',
                          className='required',
                          placeholder='Last Name')])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Employee Number: (required)'),
                dbc.Input(id='employee-number',
                          type='number',
                          className='required',
                          disabled=False,
                          placeholder='Employee Number')])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Job Code: (required)'),
                dbc.Input(id='job-code',
                          type='text',
                          className='required',
                          placeholder='Job Code')])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Level:'),
                dcc.Dropdown(id='level',
                             options=[{'label': i, 'value': i} for i in range(1, 6)],
                             placeholder='Level')])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Assigned Function:'),
                dcc.Dropdown(id='function',
                             options=[{'label': i.function, 'value': i.id}
                                      for i in sql.get_rows(Functions)],
                             placeholder='Select Function',
                             searchable=True)])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Assigned Program(s):'),
                dcc.Dropdown(id='program-name',
                             options=[{'label': i.name, 'value': i.id}
                                      for i in sql.get_rows(Program)],
                             placeholder='Select Program(s)',
                             multi=True,
                             searchable=True)])),
        dbc.Row(
            dbc.Col([
                dbc.Label('Start Date: (required)'),
                dcc.DatePickerSingle(id='start-date',
                                     with_portal=True,
                                     className='required', placeholder='Start Date',
                                     display_format='DD-MMM-YY',
                                     clearable=True,
                                     max_date_allowed=dt.datetime.today())])),
        dbc.Row(
            dbc.Col([
                dbc.Label('End Date:'),
                dcc.DatePickerSingle(id='end-date',
                                     with_portal=True,
                                     placeholder='End Date',
                                     display_format='DD-MMM-YY',
                                     clearable=True,
                                     max_date_allowed=dt.datetime.today())])),
        dbc.Row(id='edit-employee-buttons',
                children=[
                    dbc.Col(
                        dbc.Button('Add New',
                                   id='new-employee',
                                   n_clicks=0,
                                   disabled=True,
                                   style={'width': 'inherit',
                                          'margin': '2px'}),
                        width=6
                    ),
                    dbc.Tooltip('Adds a new employee to the database using the information entered in the above fields.',
                                target='new-employee'),
                    dbc.Col(
                        dbc.Button('Save',
                                   id='save-employee',
                                   n_clicks=0,
                                   style={'width': 'inherit',
                                          'margin': '2px'}),
                        width=6
                    ),
                    dbc.Tooltip('Saves any modifications to the currently selected employee record.',
                                target='save-employee'),
                    dbc.Col(
                        dbc.Button('Quick Close',
                                   id='quick-close-employee',
                                   n_clicks=0,
                                   disabled=True,
                                   style={'width': 'inherit',
                                          'margin': '2px'}),
                        width=6
                    ),
                    dbc.Tooltip('Adds end date to selected employee and creates a new record using the same date as its start date.',
                                target='quick-close-employee'),
                    dbc.Col(
                        dbc.Button('Clear',
                                   id='clear-employee-editor',
                                   n_clicks=0,
                                   style={'width': 'inherit',
                                          'margin': '2px'}),
                        width=6
                    ),
                    dbc.Tooltip('Clears the editor fields and deselects any selected rows in the table.',
                                target='clear-employee-editor'),
                ],
                style={'margin-top': '10px'}),
        dbc.Row(id='msg')]

    return editor


def employee_page_layout(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}
    if data['isadmin']:
        editor = {'width': 'auto',
                  'visibility': 'visible'}
    else:
        editor = {'width': '0px',
                  'visibility': 'hidden',
                  'padding': '0px'}

    layout = dbc.Row([
        # TODO: Create an upload area for admins so new .csv exports can be used to update the existing database
        # Employee data table
        dbc.Col([
            # Search field and buttons
            dbc.Row(
                dbc.InputGroup([
                    # Open employee editor button
                    dbc.InputGroupAddon(
                        dbc.Button(
                            html.Span([
                                html.I(className='fa fa-bars'),
                                ' Open Editor']
                            ),
                            id='open-employee-editor',
                            n_clicks_timestamp=0,
                            style=editor
                        ),
                        addon_type='prepend',
                        style={'height': '38px'}
                    ),

                    # Search field
                    dbc.Input(id='search',
                              placeholder='search employees'),
                    dbc.Tooltip('''Filter displayed employees. Comma separated search parameters can be used to refine results. eg. "name, position, title"''',
                                placement='auto-start',
                                target='search'),
                    # Clear and Search buttons
                    dbc.InputGroupAddon([
                        dbc.Button('Clear',
                                   id='clear-search',
                                   n_clicks_timestamp=0),
                        dbc.Button('Search',
                                   id='search-button',
                                   n_clicks_timestamp=0)],
                        addon_type='append',
                        style={'height': '38px'}
                    )
                ])
            ),
            # Data table
            dbc.Row(
                html.Div(
                    dcc.Loading(id='employees-loading',
                                children=[
                                    html.Div(employee_table(data),
                                             id='employee-container')
                                ],
                                type='default'
                                ),
                    style={'width': '100%',
                           'padding-top': '10px'}
                ),
                justify='between'
            )
        ],
            id='data-container'
        ),

        # Employee editor sidebar
        dbc.Col(
            dbc.Row(
                dbc.Col(
                    employee_editor(),
                    style={'height': 'auto'}
                ),
                className='sidebar',
                id='employee-editor'
            )
        )
    ])

    return layout
