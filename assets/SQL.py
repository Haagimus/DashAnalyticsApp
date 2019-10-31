from sqlalchemy.connectors import pyodbc
import pyodbc
import pandas

conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=FRXSV-DAUPHIN;DATABASE=FRXResourceDemand')


def GetTable(table):
    query = 'SELECT * from {0}'.format(table)
    results = pandas.read_sql(query, conn)
    return results


def SelectFilteredQuery(table, *args):
    pass


def InsertQuery():
    pass


def UpdateQuery():
    pass
