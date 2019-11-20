import pyodbc
import pandas
import urllib
import hashlib
import binascii
import os
from sqlalchemy import create_engine, MetaData, Table, select, inspect
from sqlalchemy.orm import sessionmaker
from assets.FRXResourceDemand import EmployeeNumber

server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'

test = 'mssql://@' + server + '/' + dbname + \
    '?trusted_connection=yes&driver=SQL+Server'


def connectEngine():
    engine = create_engine(
        'mssql://@' + server + '/' + dbname +
        '?trusted_connection=yes&driver=SQL+Server', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    return engine, session, metadata


def GetTable(tableName):
    """Gets and returns a table"""
    metadata = connectEngine()[2]
    table = metadata.tables[tableName]
    return table


def GetRows(tableName, colName):
    table = GetTable(tableName)
    session = connectEngine()[1]
    results = []
    for row in session.query(colName).all():
        results.append(row[0])

    return results


# def GetTable(name):
#     """Returns: Entire table from the database, or None if requested table
#     is not found"""
#     try:
#         results = pandas.read_sql('SELECT * FROM '+name, conn)
#     except Exception as e:
#         results = None
#     return results


# This function returns a table filtered by specified column and criteria.
def SelectQuery(table, filter):
    table = GetTable(table)
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


def InsertQuery(table, values):
    sa.insert(table=table, values=values)
    pass


def UpdateQuery():
    pass


# TODO: Create a method to register a user in the authorized user table
# TODO: Add password validation rules
def RegisterUser(Username, EmpNum, Password, Password2):
    """This will add a user to the registered user database table
       after name validation, password match validation and
       password hash occurs"""
    if Username is not None and Username is not '':
        unExists = pandas.read_sql(
            """SELECT * FROM [dbo].[RegisteredUsers]
            WHERE [Username] = '""" + Username + "' ", conn)
        if len(unExists) is not 0:
            # Username already exists in the database
            return 'Username already exists, please try a different username.'
        elif EmpNum is None or EmpNum == '':
            # No employee number has been selected
            return 'Please select an employee number to continue.'
        elif ((Password is None or Password is '') and
              (Password2 is None or Password2 is '')):
                # One or both passwords are blank
            return 'Password cannot be blank, please try again.'
        elif Password != Password2:
            # Password entries do not match
            return 'Passwords do not match, please try again.'
        else:
            # Hash the submitted password
            pwdhash = hash_password(Password)
            # Insert the entry into the registered users table
    else:
        # Username is blank
        return """Username can not be blank, please enter a username
            and try again. """

    # Account successfully added to database
    return """User account {0} has been successfully created, you may now
        log in""".format(Username)


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(Username, provided_password):
    """Verify a stored password against one provided by user"""
    if Username is not None:
        userRecord = pandas.read_sql(
            """SELECT * FROM [dbo].[RegisteredUsers]
            WHERE [Username] = '""" + Username + "' ", conn)
    else:
        return """Username can not be blank, please enter a username
            and try again."""
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
