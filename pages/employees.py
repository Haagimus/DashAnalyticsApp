# database imports
from sqlalchemy.connectors import pyodbc
from sqlalchemy.inspection import inspect
import pyodbc
# analysis imports
import pandas
import numpy
# Dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html

# Local assets import
import assets.SQL as sql

empDF = sql.GetTable('EmployeeData')
finDF = sql.GetTable('Finance_Functions')

test = sql.GetTable('EmployeeData')

count = {}
idx = 0
for title in finDF.values:
    count.update({title[0]: 0})
    for label, row in empDF.iterrows():
        if row['Function_Finance'] == title and row['Date_End'] == None:
            count[title[0]] += 1
    idx += 1

total = 0


def EmployeeTable():
    empTable = dt.DataTable(
        style_data={
            'whitespace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipses',
            'maxWidth': 0,
        },
        id='Employees',
        columns=[
            {'name': i, 'id': i, 'selectable': True} for i in empDF.columns
        ],
        data=empDF.to_dict('records'),
        editable=True,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        row_deletable=False,
        hidden_columns=['Name_Full'],
    ),
    html.Div(id='employee-container')
    return empTable

# For debugging
# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
