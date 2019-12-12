import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import dash_table as dt
import assets.SQL as sql
import assets.models as models
import plotly.express as px
import dash_ui as dui

employees = sql.get_rows(models.EmployeeData)
functions = sql.get_rows(models.Functions)


def function_totals():
    count = {}
    idx = 0
    total = 0
    for item in functions:
        count.update({item.function: 0})
        for row in employees:
            if row.assigned_function == item.function and row.date_end is None:
                count[item.function] += 1
                total += 1
        idx += 1
    count.update({'Total': total})

    results = pd.DataFrame({
        'Functions': list(count.keys()),
        'Head Count': list(count.values())
    })

    return results


def functions_chart():
    count = {}
    idx = 0
    for item in functions:
        count.update({item.function: 0})
        for row in employees:
            if row.assigned_function == item.function and row.date_end is None:
                count[item.function] += 1
        idx += 1

    results = pd.DataFrame({
        'Functions': list(count.keys()),
        'Head Count': list(count.values())
    })
    graph = dcc.Graph(id='functions-graph',
                      figure={
                          'data': [{'x': results['Functions'], 'type': 'bar',
                                    'y': results['Head Count'], 'type': 'bar'}]
                      }
                      )

    return graph


def capacity():
    ft = function_totals()

    content = dbc.Row([
        dbc.Col([
            html.H1('Functional Area Totals:',
                    style={'color': 'white',
                           'text-align': 'center'}),
            dt.DataTable(
                id='capacity',
                columns=[{'name': i, 'id': i} for i in ft],
                data=ft.to_dict('rows'),
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bolder',
                    'fontSize': '18px',
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'},
                    {'if': {'row_index': 15},
                     'fontWeight': 'bolder',
                     'fontSize': '18px'},
                    {'if': {'column_id': 'Functions'},
                     'textAlign': 'right',
                     'padding': '5px 15px 5px 0px'},
                    {'if': {'column_id': 'Head Count'},
                     'textAlign': 'left',
                     'padding': '5px 0px 5px 15px'}
                ]
            )
        ],
            width=4),
        dbc.Col([
            html.H1('Graph',
                    style={'color': 'white',
                           'text-align': 'center'}),
            functions_chart()
        ],
            width=8)
    ])

    return content
