import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import assets.SQL as sql
from assets.models import ProjectData, EmployeeData

employees = sql.get_rows(EmployeeData)

edit_employee_modal = dbc.Modal([
    dbc.ModalHeader('Employee Data:', id='loginHead'),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Label('First Name: *'),
                dbc.Input(id='first-name',
                          type='text',
                          className='required',
                          placeholder='First Name')]),
            dbc.Col([
                dbc.Label('Last Name: *'),
                dbc.Input(id='last-name',
                          type='text',
                          className='required',
                          placeholder='Last Name')])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label('Employee Number: *'),
                dbc.Input(id='employee-number',
                          type='number',
                          className='required',
                          placeholder='Employee Number')]),
            dbc.Col([
                dbc.Label('Job Code: *'),
                dbc.Input(id='job_code',
                          type='text',
                          className='required',
                          placeholder='Job Code')])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label('Assigned Project(s)'),
                dcc.Dropdown(id='project-name',
                             options=[{'label': i.name, 'value': i.id}
                                      for i in sql.get_rows(ProjectData)],
                             placeholder='Select project(s)',
                             multi=True,
                             searchable=True)]),
            dbc.Col([
                dbc.Input(id='first-name',
                          type='text',
                          className='required',
                          placeholder='First Name')])
        ])
    ]),
    dbc.ModalFooter([
        dbc.Col(
            dbc.Button('Delete',
                       id='employeeDelete',
                       color='danger',
                       n_clicks=0,
                       n_clicks_timestamp=0),
            width=8,
            style={'padding-left': '0px'}
        ),
        dbc.Col([
            dbc.Button('Save',
                       id='employeeDataSave',
                       n_clicks=0,
                       n_clicks_timestamp=0,
                       style={'margin': '0px 2px'}),
            dbc.Button('Close',
                       id='employeeEditorClose',
                       n_clicks=0,
                       style={'margin': '0px 2px'})
        ],
            width='auto',
            style={'padding-right': '0px'}
        )
    ])
],
    id='employeeDataModel'
)


def employee_page_layout(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}
    if data['isadmin']:
        layout = dbc.Col([
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
            dbc.Row([
                dbc.Button('New Employee', id='new-employee', n_clicks_timestamp=0),
                dbc.Button('Edit Employee', id='edit-employee', n_clicks_timestamp=0)
            ],
                justify='between',
                style={'padding': '10px 0px'}
            ),
            dbc.Row(
                html.Div(
                    dcc.Loading(id='employees-loading',
                                children=[
                                    html.Div(id='employee-container')
                                ],
                                type='default'
                                ),
                    style={'width': '100%'}
                ),
                justify='between'
            ),
            edit_employee_modal
        ])
    else:
        layout = dbc.Col([
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
                                    html.Div(id='employee-container')
                                ],
                                type='default'
                                ),
                    style={'width': '100%',
                           'padding-top': '10px'}
                ),
                justify='between'
            )
        ])
    return layout
