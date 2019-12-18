import binascii
import hashlib
import os
from collections import defaultdict

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker

from assets.models import EmployeeData, RegisteredUser

server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'
engine = create_engine('mssql://@{0}/{1}?trusted_connection=yes&driver=SQL+Server'.format(server, dbname), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
metadata.reflect(bind=engine)

emp_cols_str = [EmployeeData.name_first,
                EmployeeData.name_last,
                EmployeeData.job_title,
                EmployeeData.assigned_function,
                EmployeeData.assigned_programs,
                EmployeeData.job_code]
emp_cols_int = [EmployeeData.employee_number,
                EmployeeData.date_end,
                EmployeeData.date_start]


def get_rows(table_name):
    """
    Returns all rows from selected columns in a table
    :param table_name: str
    :return: list[]
    """
    results = session.query(table_name).all()
    return results


def query_rows(table_name, param):
    results = []
    if param is None:
        return get_rows(table_name)

    try:
        param = int(param)
        for item in emp_cols_int:
            if len(session.query(table_name).filter(item.like('%{}%'.format(param))).all()) > 0:
                for i in session.query(table_name).filter(item.like('%{}%'.format(param))).all():
                    results.append(i)
                    continue
    except ValueError:
        for item in emp_cols_str:
            if len(session.query(table_name).filter(item.like('%{}%'.format(param))).all()) > 0:
                for i in session.query(table_name).filter(item.like('%{}%'.format(param))).all():
                    results.append(i)
                    continue

    # results = query_to_dict(results)
    return results


def query_to_list(result_set):
    """
    List conversion from sqlalchemy query
    :param result_set: query
    :return: list[]
    """
    results = []
    for obj in result_set:
        instance = inspect(obj)
        items = instance.attrs.items()
        results.append([x.value for _, x in items])
    return instance.attrs.keys(), results


def query_to_dict(result_set):
    """
    Dictionary conversion from sqlalchemy query
    :param result_set: query
    :return: dict
    """
    result = defaultdict(list)
    for row in result_set:
        instance = inspect(row)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


def register_user(username, emp_num, password, password2):
    """
    This will add a user to the registered user database table
       after name validation, password match validation and
       password hash occurs
    :param username: str
    :param emp_num: int
    :param password: str
    :param password2: str
    :return: str
    """
    if username is not None and username is not '':
        uname = session.query(RegisteredUser).filter(RegisteredUser.username == username).first()
        empnum = session.query(RegisteredUser).filter(RegisteredUser.employee_number == emp_num).first()
        if uname is not None:
            return 'Username already exists, please try a different username.'
        elif emp_num is None or emp_num == '':
            # No employee number has been selected
            return 'Please select an employee number to continue.'
        elif empnum is not None:
            # employee number already has an account
            return 'Employee number already has associated account.'
        elif ((password is None or password is '') and
              (password2 is None or password2 is '')):
            # One or both passwords are blank
            return 'Password cannot be blank, please try again.'
        elif password != password2:
            # Password entries do not match
            return 'Passwords do not match, please try again.'
        else:
            # Hash the submitted password
            pwdhash = hash_password(password)
            # Insert the entry into the registered users table
            add_user(username, pwdhash, emp_num)
    else:
        # Username is blank
        return """Username can not be blank, please enter a username
            and try again. """

    # Account successfully added to database
    return """User account {0} has been successfully created, you may now
        log in""".format(username)


def add_user(username, password, emp_num):
    """
    Adds a new user to the registered user table
    :param username: str
    :param password: str
    :param emp_num: int
    :return: None
    """
    submission = RegisteredUser(username=username,
                                employee_number=emp_num,
                                password=password)
    session.add(submission)
    session.commit()


def hash_password(password):
    """
    Hash a password for storing
    :param password: str
    :return: str
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(username, provided_password):
    """
    Verify a stored password against one provided by user
    :param username: str
    :param provided_password: str
    :return: str
    """
    if username is not None:
        results = session.query(RegisteredUser).filter(RegisteredUser.username == username).first()
    else:
        return """Username can not be blank, please enter a username
            and try again."""

    if provided_password is None:
        return """Password can not be blank, please enter a password
            and try again."""
    if results is None:
        return 'User not found'
    stored_password = results.password
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    if pwdhash == stored_password:
        return results
    else:
        return 'Invalid Password'
