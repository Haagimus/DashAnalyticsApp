from sqlalchemy.connectors import pyodbc
from sqlalchemy.inspection import inspect
import pyodbc
import pandas

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

# for (key, value) in count.items():
#     print(key, '::', value)
#     total += value
# print('{0} total staff'.format(total))
