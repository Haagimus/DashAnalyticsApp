import pyodbc
import pandas

# sqlalchemy imports
from sqlalchemy.sql import table, select

conn = pyodbc.connect(
    'DRIVER={SQL Server};SERVER=FRXSV-DAUPHIN;DATABASE=FRXResourceDemand')


# This function returns an entire table. If the table requested is not found the 'None' value is returned.
def GetTable(name):
    try:
        t = table('dbo.' + name)
        results = conn.execute(t)
    except:
        results = None
    return results


# This function returns a table filtered by specified column and criteria.
# Len(results) == 0 if no matches are found.
def SelectQuery(columns=None, whereclause=None, from_obj=None, distinct=False, having=None, correlate=True, prefixes=None, suffixes=None):

    # results = pandas.read_sql(query, conn)
    # return results
    pass


def MultiSelectQuery(table, columns, criteria):
    # if type(columns) == list and type(criteria) == list:
    #     if len(columns) != len(criteria):
    #         return None
    #     else:
    #         cList = 'OR'.join(columns, criteria)

    # for c in criteria:
    #     if cList == None:
    #         cList = c
    #     else:
    #         cList = cList + ', {0}'.format(c)
    # query = 'SELECT * FROM dbo.{0} WHERE {1}=\'{2}\''.format(
    #     table, columns, cList)
    # results = pandas.read_sql(query, conn)
    # return results
    pass


def InsertQuery():
    pass


def UpdateQuery():
    pass
