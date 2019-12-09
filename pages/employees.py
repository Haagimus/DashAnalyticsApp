# analysis imports
import pandas
import numpy
# Dash
import dash_table as dt
import dash_html_components as html
from dash.dependencies import Output, Input
from server import app

# Local assets import
import assets.SQL as sql
import assets.models as models

employees = sql.get_rows(models.EmployeeData)
functions = sql.get_rows(models.Functions)


def function_totals():
    count = {}
    idx = 0
    for item in functions:
        count.update({item.function:0})
        for row in employees:
            if row.assigned_function == item.function and row.date_end is None:
                count[item.function] += 1
        idx += 1

    results = pandas.DataFrame({
        'Functions': list(count.keys()),
        'Head Count': list(count.values())
    })

    return results


def employee_page_layout():
    layout = dt.DataTable(
        style_data={
            'whitespace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipses',
            'maxWidth': 0
        },
        id='Employees',
        columns=[{'name': i, 'id': i} for i in dir(models.EmployeeData) if not i.startswith('_')],
        data=[{'name_first': i.name_first,
               'name_last': i.name_last,
               'function': i.function,
               'functions': i.functions,
               'job_code': i.job_code,
               'programs': i.programs,
               'date_start': i.date_start} for i in employees],
        editable=False,
        filter_action='custom',
        sort_action='native',
        sort_mode='single',
        row_deletable=False,
        hidden_columns=[
            'id',
            'metadata',
            'is_admin',
            'level',
            'number',
            'employee_number',
            'assigned_function',
            'assigned_programs',
            'job_title',
            'date_end'],
        style_as_list_view=True,
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        row_selectable='single'
    ),
    html.Div(id='employee-container')
    return layout


# For debugging
# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
