import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt

import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)

basic_columns = [{'name': 'First Name', 'id': 'name_first'},
                 {'name': 'Last Name', 'id': 'name_last'},
                 {'name': 'Job Code', 'id': 'job_code'},
                 {'name': 'Assigned Function', 'id': 'function'},
                 {'name': 'Assigned Program', 'id': 'programs'},
                 {'name': 'Start Date', 'id': 'date_start'}]

basic_data = [{'name_first': i.name_first,
               'name_last': i.name_last,
               'function': i.assigned_function,
               'job_code': i.job_code,
               'programs': i.programs,
               'date_start': i.date_start} for i in employees]


# filtering will apply for i in employees if param == search


# TODO: Add admin layout columns and data


def employee_page_layout(admin):
    if admin:
        layout = dbc.Col([
            'test'
        ])
    else:
        layout = dbc.Col([
            dbc.InputGroup([
                dbc.Input(id='search', placeholder='search employees'),
                dbc.InputGroupAddon([
                    dbc.Button('Clear', id='clear-search'),
                    dbc.Button('Search', id='search-button')],
                    addon_type='append'
                )
            ]),
            html.Br(),
            dt.DataTable(
                id='Employees',
                # style_data={
                #     'whitespace': 'normal',
                #     'height': 'auto',
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipses',
                #     'maxWidth': 0
                # },
                columns=basic_columns,
                data=basic_data,
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
            ),
            html.Div(id='employee-container')
        ])
    return layout

# TODO: Add a callback to filter the employee table
