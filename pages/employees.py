import datetime

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt

import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)


def employee_page_layout(admin):
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

        html.Div(id='employee-container')
    ])

    return layout

# TODO: Add a callback to filter the employee table
