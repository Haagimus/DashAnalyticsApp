import pyodbc
import pandas
import urllib
import hashlib
import binascii
import os
from sqlalchemy import create_engine, MetaData, Table, select, inspect
from sqlalchemy.orm import sessionmaker
import assets.FRXResourceDemand as frxrd

server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'


def connectEngine():
    engine = create_engine(
        'mssql://@' + server + '/' + dbname +
        '?trusted_connection=yes&driver=SQL+Server', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)

    return engine, session, metadata


class Engine:
    def __init__(self, engine, session, metadata):
        self.engine = engine
        self.session = session
        self.metadata = metadata

engine = Engine(connectEngine()[0], connectEngine()[1], connectEngine()[2])


def GetRows(tableName):
    """Retruns all rows from selected columns in a table"""
    table = engine.metadata.tables[tableName]
    session = engine.session
    results = session.query(table).all()
    return results


# TODO: Create a method to register a user in the authorized user table
# TODO: Add password validation rules
def RegisterUser(Username, EmpNum, Password, Password2):
    """This will add a user to the registered user database table
       after name validation, password match validation and
       password hash occurs """
    userList = GetRows('RegisteredUsers', frxrd.RegisteredUser.Username)
    session = engine.session
    if Username is not None and Username is not '':
        q = session.query(userList).filter(userList.Username == Username)
        if session.query(q.exists()):
            # unExists = pandas.read_sql(
            #     """SELECT * FROM [dbo].[RegisteredUsers]
            #     WHERE [Username] = '""" + Username + "' ", engine)
            # if len(unExists) is not 0:
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
            WHERE [Username] = '""" + Username + "' ", engine)
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
