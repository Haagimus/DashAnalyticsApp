import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

import assets.SQL as sql
from assets.models import EmployeeFunctionLink, EmployeeData

functions = sql.get_rows(EmployeeFunctionLink)
dfmt = '%b-%y'


def get_counts():
    count = {}
    employees = sql.get_rows(EmployeeData)
    ended = []

    for row in employees:
        if row.date_end is not None:
            ended.append(row)

    active_employees = [e for e in employees if e not in ended]

    for f in functions:
        count.update({f.employee_function: 0})
        for row in active_employees:
            if row.employee_number.assigned_functions[0].function == f.employee_function:
                count[f.employee_function] += 1
    count.update({'Total': len(active_employees)})

    return count


def function_totals():
    count = get_counts()

    results = pd.DataFrame({
        'Functions': list(count.keys()),
        # 'Head Count': list(count.values()),
        (date.today() + relativedelta(months=-3)).strftime(dfmt).upper(): list(count.values()),
        (date.today() + relativedelta(months=-2)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=-1)).strftime(dfmt).upper(): '',
        (date.today()).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+1)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+2)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+3)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+4)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+5)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+6)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+7)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+8)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+9)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+10)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+11)).strftime(dfmt).upper(): '',
        (date.today() + relativedelta(months=+12)).strftime(dfmt).upper(): ''
    })

    return results


def functions_chart():
    count=get_counts()
    count.pop('Total')

    results=pd.DataFrame({
        'Functions': list(count.keys()),
        'Head Count': list(count.values())
    })
    graph=dcc.Graph(id='functions-graph',
                      figure={
                          'data': [{'x': results['Functions'], 'type': 'bar',
                                    'y': results['Head Count'], 'type': 'bar'}]
                      }
                      )

    return graph


def capacity_page_layout():
    totals=function_totals()

    layout=dbc.Row([
        dbc.Col(
            dt.DataTable(
                id='capacity',
                columns=[{'name': i, 'id': i} for i in totals],
                data=totals.to_dict("rows"),
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bolder',
                    'fontSize': '16px',
                    'textAlign': 'center'
                },
                style_data={
                    'textAlign': 'center',
                    'fontSize': '12px',
                    'fontWeight': 'bold',
                    'height': 'auto',
                    'width': 'auto'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'},
                     'backgroundColor': 'rgb(248, 248, 248)'},
                    {'if': {'row_index': len(totals) - 1},
                     'fontWeight': 'bolder',
                     'fontSize': '16px'},
                    {'if': {'column_id': 'Functions'},
                     'textAlign': 'right',
                     'padding': '0px 15px 0px 0px',
                     'fontSize': '12px'}
                ]
            ),
            width=12
        ),
        dbc.Col(
            functions_chart(),
            width=12
        )
    ])
    return layout
