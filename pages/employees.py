import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)


def employee_page_layout(data=None):
    if data is None:
        data = {'isadmin': False,
                'logged_in': False,
                'login_user': None}
    if data['isadmin']:
        layout = dbc.Col([
            dbc.InputGroup([
                dbc.Input(id='search', placeholder='search employees'),
                dbc.InputGroupAddon([
                    dbc.Button('Clear', id='clear-search', n_clicks_timestamp=0),
                    dbc.Button('Search', id='search-button', n_clicks_timestamp=0)],
                    addon_type='append'
                )
            ]),
            html.Br(),
            html.Div(
                dcc.Loading(id='employees-loading',
                            children=[
                                html.Div(id='employee-container')
                            ],
                            type='default'
                            ))
        ])
    else:
        layout = dbc.Col([
            dbc.InputGroup([
                dbc.Input(id='search', placeholder='search employees'),
                dbc.InputGroupAddon([
                    dbc.Button('Clear', id='clear-search', n_clicks_timestamp=0),
                    dbc.Button('Search', id='search-button', n_clicks_timestamp=0)],
                    addon_type='append'
                )
            ]),
            html.Br(),
            html.Div(
                dcc.Loading(id='employees-loading',
                            children=[
                                html.Div(id='employee-container')
                            ],
                            type='default'
                            ))
        ])
    return layout
