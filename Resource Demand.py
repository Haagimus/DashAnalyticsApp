from sqlalchemy.connectors import pyodbc
from sqlalchemy.inspection import inspect
import pyodbc
import pandas
import numpy
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html

EmpTblSQL = 'SELECT * FROM dbo.Employees'
FinTblSql = 'SELECT * FROM dbo.Finance_Functions'
HRTblSQL = 'SELECT * FROM dbo.HR_Functions'

conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=FRXSV-DAUPHIN;DATABASE=FRXResourceDemand')

empDF = pandas.read_sql(EmpTblSQL, conn)
finDF = pandas.read_sql(FinTblSql, conn)
hrDF = pandas.read_sql(HRTblSQL, conn)

count = {}
idx = 0
for title in finDF.values:
    count.update({title[0]: 0})
    for label, row in empDF.iterrows():
        if row['Function_Finance'] == title and row['Date_End'] == None:
            count[title[0]] += 1
    idx += 1

total = 0
for (key, value) in count.items():
    print(key, '::', value)
    total += value
print('{0} total staff'.format(total))

app = dash.Dash(__name__)

app.layout = html.Div([
    dt.DataTable(
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
        hidden_columns=['Long_Text', 'Name_Full'],
    ),
    html.Div(id='employee-container')
])

if __name__ == '__main__':
    app.run_server(debug=False)
