# analysis imports
import pandas
import numpy
# Dash
import dash_table as dt
import dash_html_components as html

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
            if row[0][5] == item[0] and row[0][9] == None:
                count[item[0]] += 1
        idx += 1

    total = 0
    return count, total


def EmployeeTable():
    empTable = dt.DataTable(
        style_data={
            'whitespace': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipses',
            'maxWidth': 0,
            'back'
        },
        id='Employees',
        columns=[{'name': i, 'id': i} for i in empDF.columns],
        data=empDF.to_dict('records'),
        editable=True,
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        row_deletable=False,
        hidden_columns=[
            'Name_Full',
            'IsAdmin',
            'Level',
            'Employee_Number',
            'Job_Title',
            'Date_End',
            'Acting'],
    ),
    html.Div(id='employee-container')
    return empTable

# For debugging
# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
