# analysis imports
import pandas
import numpy
# Dash
import dash_table as dt
import dash_html_components as html
from dash.dependencies import Output, Input

# Local assets import
import assets.SQL as sql

empDF = sql.GetTable('EmployeeData')
finTbl = sql.GetTable('Finance_Functions')


def funcTotals():
    count = {}
    idx = 0
    for item in finTbl:
        count.update({item[0]: 0})
        for row in empDF.values:
            if row[0][5] == item[0] and row[0][9] is None:
                count[item[0]] += 1
        idx += 1

    total = 0
    return count, total


layout = dt.DataTable(
    style_data={
        'whitespace': 'normal',
        'height': 'auto',
        'overflow': 'hidden',
        'textOverflow': 'ellipses',
        'maxWidth': 0
    },
    id='Employees',
    columns=[{'name': i, 'id': i} for i in empDF.columns],
    data=empDF.to_dict('records'),
    editable=False,
    filter_action='custom',
    sort_action='native',
    sort_mode='single',
    row_deletable=False,
    hidden_columns=[
        'Name_Full',
        'IsAdmin',
        'Level',
        'Employee_Number',
        'Job_Title',
        'Date_End',
        'Acting'],
    style_as_list_view=True,
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    },
    row_selectable='single'
),
html.Div(id='employee-container')


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1:-1].replace('\\' + v0. v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

# For debugging
# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
