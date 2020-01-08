import binascii
import hashlib
import os
from collections import defaultdict

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.orm import sessionmaker

from assets.models import RegisteredUser, EmployeeData, ProjectData, Functions

server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'
engine = create_engine('mssql://@{0}/{1}?trusted_connection=yes&driver=SQL+Server'.format(server, dbname), echo=False)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

emp_cols = {0: (EmployeeData, EmployeeData.name_first),
            1: (EmployeeData, EmployeeData.name_last),
            2: (EmployeeData, EmployeeData.job_title),
            3: (Functions, Functions.function),
            4: (ProjectData, ProjectData.name),
            5: (EmployeeData, EmployeeData.job_code),
            6: (EmployeeData, EmployeeData.employee_number_number),
            7: (EmployeeData, EmployeeData.date_end),
            8: (EmployeeData, EmployeeData.date_start),
            9: (EmployeeData, EmployeeData.level)}


def get_rows(class_name):
    """
    Returns all rows from selected columns in a table
    :param class_name: str
    :return: list[]
    """
    results = session.query(class_name).all()
    return results


def query_rows(filter_text):
    """

    :param filter_text: str
    :return: []
    """
    results = []

    try:
        filter_text = int(filter_text)
    except ValueError:
        filter_text = filter_text

    for idx, column in emp_cols.items():
        if isinstance(filter_text, int):
            if len(session.query(column[0]).filter(column[1].contains('%{}%'.format(filter_text))).all()) > 0:
                for i in session.query(column[0]).filter(column[1].contains('%{}%'.format(filter_text))).all():
                    if not isinstance(i, EmployeeData):
                        for emp in i.employee_number:
                            results.append(emp.employee_data[0])
                    else:
                        results.append(i)
        elif isinstance(filter_text, str):
            if len(session.query(column[0]).filter(column[1].like(filter_text)).all()) > 0:
                for i in session.query(column[0]).filter(column[1].like(filter_text)).all():
                    if isinstance(i, ProjectData):
                        for emp in i.employee_number:
                            results.append(emp.employee_data[0])
                    elif isinstance(i, Functions):
                        for emp in i.employees:
                            results.append(emp.employee_data[0])
                    else:
                        results.append(i)

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
    :return: str or RegisteredUser
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
