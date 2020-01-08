import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd

import assets.SQL as sql
from assets.models import employee_function_association_table, EmployeeData

employees = sql.get_rows(EmployeeData)
functions = sql.get_rows(employee_function_association_table)


def function_totals():
    count = {}
    total = 0
    for f in functions:
        count.update({f.function_name: 0})
        for row in employees:
            if row.employee_number.assigned_functions[0].function == f.function_name and row.date_end is None:
                count[f.function_name] += 1
        total += 1
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
        count.update({item.function_name: 0})
        for row in employees:
            if row.employee_number.assigned_functions[0].function == item.function_name and row.date_end is None:
                count[item.function_name] += 1
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


def capacity_page_layout():
    layout = dbc.Row([
        dbc.Col(
            # html.H2('Functional Area Totals:',
            #         style={'text-align': 'center'}),
            dt.DataTable(
                id='capacity',
                columns=[{'name': i, 'id': i} for i in function_totals()],
                data=function_totals().to_dict('rows'),
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bolder',
                    'fontSize': '16px',
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'},
                    {'if': {'row_index': 25},
                     'fontWeight': 'bolder',
                     'fontSize': '16px'},
                    {'if': {'column_id': 'Functions'},
                     'textAlign': 'right',
                     'padding': '2px 15px 2px 0px'},
                    {'if': {'column_id': 'Head Count'},
                     'textAlign': 'left',
                     'padding': '2px 0px 2px 15px'}
                ]
            ),
            xs={'size': 12, 'order': 1},
            md={'size': 6, 'order': 2},
            lg={'size': 5, 'order': 1}),
        dbc.Col([
            functions_chart()
        ],
            xs={'size': 12, 'order': 2},
            md={'size': 12, 'order': 1},
            lg={'size': 7, 'order': 2})
    ])

    return layout
