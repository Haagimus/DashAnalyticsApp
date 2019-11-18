import pyodbc
import pandas
import urllib
import hashlib
import binascii
import os

# sqlalchemy imports
from sqlalchemy.sql import table, select

driver = 'SQL Server'
server = 'FRXSV-DAUPHIN'
database = 'FRXResourceDemand'

try:
    conn = pyodbc.connect(
        'DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';')

    cursor = conn.cursor()
except:
    pass


# This function returns an entire table. If the table requested is not found
# the 'None' value is returned.
def GetTable(name):
    """Returns an entire table from the database"""
    try:
        results = pandas.read_sql('SELECT * FROM '+name, conn)
        # cursor.execute('SELECT * FROM '+name)
        # results = cursor.fetchall()
    except:
        results = None
    return results


# This function returns a table filtered by specified column and criteria.
# Len(results) == 0 if no matches are found.
def SelectQuery(columns=None, whereclause=None, from_obj=None, distinct=False,
                having=None, correlate=True, prefixes=None, suffixes=None):

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


def RegisterUser(Username, Password):
    """This will add a user to the registered user database table
       after name validation and password hash occurs"""
    pwdhash = hash_password(password)
    pass


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(Username, provided_password):
    """Verify a stored password against one provided by user"""
    userRecord = pandas.read_sql(
        """SELECT * FROM [dbo].[RegisteredUsers]
        WHERE [Username] = '""" + Username + "'", conn)
    if len(userRecord) == 0:
        return 'User not found'
    stored_password = userRecord['Password'][0]
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    if pwdhash == stored_password:
        return 'Logged in as {0}'.format(userRecord['Username'][0])
    else:
        return 'Invalid Password'

# TODO: Create a method to register a user in the authorized user table
# TODO: Add username validation
# TODO: Add password validation rules
