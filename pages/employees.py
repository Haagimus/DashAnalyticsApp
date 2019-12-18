import datetime

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt

import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)


def get_columns(admin):
    if not admin:
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'}]
    else:
        columns = [{'name': 'First Name', 'id': 'name_first'},
                   {'name': 'Last Name', 'id': 'name_last'},
                   {'name': 'Job Code', 'id': 'job_code'},
                   {'name': 'Assigned Function', 'id': 'function'},
                   {'name': 'Assigned Program', 'id': 'programs'},
                   {'name': 'Start Date', 'id': 'date_start'},
                   {'name': 'End Date', 'id': 'date_end'}]
    return columns


def get_data(admin):
    if not admin:
        data = [{'name_first': i.name_first,
                 'name_last': i.name_last,
                 'function': i.assigned_function,
                 'job_code': i.job_code,
                 'programs': i.programs,
                 'date_start': i.date_start} for i in employees]
    else:
        data = [{'name_first': i.name_first,
                 'name_last': i.name_last,
                 'function': i.assigned_function,
                 'job_code': i.job_code,
                 'programs': i.programs,
                 'date_start': i.date_start} for i in employees]
    return data


def employee_page_layout(admin):
    columns = get_columns(admin)
    data = get_data(admin)

    layout = dbc.Col([
        dbc.InputGroup([
            dbc.Input(id='search', placeholder='search employees'),
            dbc.InputGroupAddon([
                dbc.Button('Clear', id='clear-search', n_clicks_timestamp=0),
                dbc.Button('Search', id='search-button', n_clicks_timestamp=0)],
                addon_type='append'
            )
        ],
            id='submit-group'),
        html.Br(),
        # dt.DataTable(
        #     id='Employees',
        #     columns=columns,
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
        #     row_selectable='single'
        # ),
        html.Div(id='employee-container')
    ])

    return layout

# TODO: Add a callback to filter the employee table
