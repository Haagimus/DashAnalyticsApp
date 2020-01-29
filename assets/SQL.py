import binascii
import hashlib
import os
from collections import defaultdict

from sqlalchemy import create_engine, MetaData, inspect, update
from sqlalchemy.orm import sessionmaker

from assets.models import RegisteredUser, EmployeeData, ProjectData, Functions, Program, EmployeeNumber, EmployeeFunctionLink, EmployeeProgramLink
from server import app, log_time

server = 'FRXSV-DAUPHIN'
dbname = 'FRXResourceDemand'
t_conn = 'trusted_connections=yes'
driver = 'driver=SQL+Server'
MARS = 'MARS_Connection=Yes'
echo = False
pool_size = 20
engine = create_engine(f'mssql://@{server}/{dbname}?{t_conn}&{driver}&{MARS}',
                       echo=echo,
                       pool_size=pool_size)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)

emp_cols = {0: (EmployeeData, EmployeeData.name_first),
            1: (EmployeeData, EmployeeData.name_last),
            2: (EmployeeData, EmployeeData.job_title),
            3: (Functions, Functions.function),
            4: (Program, Program.name),
            5: (EmployeeData, EmployeeData.job_code),
            6: (EmployeeData, EmployeeData.employee_number_number),
            7: (EmployeeData, EmployeeData.date_end),
            8: (EmployeeData, EmployeeData.date_start),
            9: (EmployeeData, EmployeeData.level)}


def get_rows(class_name, filter_text=None):
    """
    Returns all rows from selected columns in a table
    :param class_name: str
    :param filter_text: str
    :return: list[]
    """
    session.rollback()
    if filter_text is None:
        results = session.query(class_name).all()
    else:
        results = session.query(class_name).filter(filter_text).all()
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
                        for emp in i.employee_number_number:
                            if emp.employee_data[0] not in results:
                                results.append(emp.employee_data[0])
                    else:
                        if i not in results:
                            results.append(i)
        elif isinstance(filter_text, str):
            if len(session.query(column[0]).filter(column[1].contains('%{}%'.format(filter_text))).all()) > 0:
                for i in session.query(column[0]).filter(column[1].contains('%{}%'.format(filter_text))).all():
                    if isinstance(i, Program):
                        for emp in i.employees:
                            if emp.employee_data[0] not in results:
                                results.append(emp.employee_data[0])
                    elif isinstance(i, Functions):
                        for emp in i.employees:
                            if emp.employee_data[0] not in results:
                                results.append(emp.employee_data[0])
                    else:
                        if i not in results:
                            results.append(i)
    session.close()
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
        try:
            empnum = session.query(RegisteredUser).filter(RegisteredUser.employee_number == emp_num).first()
        except AttributeError:
            empnum = None
        if uname is not None:
            app.logger.info(f'INFO :: Registration Failed :: Username, {uname}, already exists.')
            return 'Username already exists, please try a different username.'
        elif emp_num is None or emp_num == '':
            # No employee number has been selected
            app.logger.info('INFO :: Registration Failed :: No employee number selected.')
            return 'Please select an employee number to continue.'
        elif empnum is not None:
            # employee number already has an account
            return 'Employee number already has associated account.'
        elif ((password is None or password is '') and
              (password2 is None or password2 is '')):
            # One or both passwords are blank
            app.logger.info('INFO :: Registration Failed :: One or both password fields were blank.')
            return 'Password cannot be blank, please try again.'
        elif password != password2:
            # Password entries do not match
            app.logger.info('INFO :: Registration Failed :: Entered passwords did not match.')
            return 'Passwords do not match, please try again.'
        else:
            # Hash the submitted password
            pwdhash = hash_password(password)
            # Insert the entry into the registered users table
            add_user(username, pwdhash, emp_num)
    else:
        # Username is blank
        app.logger.info('INFO :: Registration Failed :: Username was blank.')
        return 'Username can not be blank, please enter a username and try again.'

    # Account successfully added to database
    app.logger.info(f'INFO :: Registration Success :: Account created for {username} with employee number {emp_num}.')
    return f'User account {username} has been successfully created, you may now log in'


def add_user(username, password, emp_num):
    """
    Adds a new user to the registered user table
    :param username: str
    :param password: str
    :param emp_num: int
    :return: None
    """
    empnum = session.query(EmployeeNumber).filter(EmployeeNumber.id == emp_num).first()
    query = EmployeeFunctionLink.employee_number == empnum.number
    func = get_rows(EmployeeFunctionLink, query)

    submission = RegisteredUser(username=username, employee_number=empnum, function=func[0].employee_function, password=password)
    session.add(submission)
    session.commit()


def add_employee(first_name, last_name, employee_number, job_code, level, func, pgms, start_date, end_date):
    """
    Adds a new employee to the EmployeeData table
    :param first_name: str
    :param last_name: str
    :param employee_number: int
    :param job_code: str
    :param level: inf
    :param func: str
    :param pgms: str
    :param start_date: date
    :param end_date: date
    :return: None
    """
    number = (EmployeeNumber(number=employee_number))

    try:
        session.add(number)
        session.commit()
    except Exception as e:
        if 'Cannot insert duplicate key' in e.args[0]:
            app.logger.error(f'ERROR :: Add Employee Failed :: {employee_number} already exists in the table EmployeeNumber.')
        session.rollback()
        raise
    finally:
        session.close()

    queries = []

    function_name = session.query(Functions).filter(Functions.id == func)[0].function
    queries.append(EmployeeFunctionLink.insert().values(function_name=function_name, employee_number=employee_number))

    pgm_names = []
    for p in pgms:
        pgm_names.append(session.query(Program).filter(Program.id == p)[0].name)

    for p in pgm_names:
        queries.append(EmployeeProgramLink.insert().values(program_name=p, employee_number=employee_number))

    for q in queries:
        try:
            session.execute(q)
            session.commit()
        except Exception as e:
            app.logger.error(f'ERROR :: [{e.errno}] :: {e.strerror}')
            session.rollback()
            raise
        finally:
            session.close()

    employee = EmployeeData(name_first=first_name, name_last=last_name, employee_number_number=employee_number, job_code=job_code,
                            level=level, date_start=start_date, date_end=end_date)
    try:
        session.add(employee)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: [{e.errno}] :: {e.strerror}')
        session.rollback()
        raise
    finally:
        session.close()


def update_employee(employee_number, **kwargs):
    """
    Update an existing employee data entry
    :keyword name_first: str
    :keyword name_last: str
    :keyword employee_number: int
    :keyword job_code: str
    :keyword level: int
    :keyword assigned_function: str
    :keyword assigned_programs: []
    :keyword date_start: date
    :keyword date_end: date
    """
    session.rollback()
    employee = session.query(EmployeeData).filter(EmployeeData.employee_number_number == employee_number).first()

    if kwargs.__contains__('name_first'):
        if kwargs['name_first']:
            employee.name_first = kwargs['name_first']
        else:
            employee.name_first = None

    if kwargs.__contains__('name_last'):
        if kwargs['name_last']:
            employee.name_last = kwargs['name_last']
        else:
            employee.name_last = None

    if kwargs.__contains__('employee_number'):
        if kwargs['employee_number']:
            employee.employee_number_number = kwargs['employee_number']
        else:
            employee.employee_number_number = None

    if kwargs.__contains__('job_code'):
        if kwargs['job_code']:
            employee.job_code = kwargs['job_code']
        else:
            employee.job_code = None

    if kwargs.__contains__('level'):
        if kwargs['level']:
            employee.level = kwargs['level']
        else:
            employee.level = None

    if kwargs.__contains__('function'):
        if kwargs['function']:
            session.query(EmployeeFunctionLink).filter(EmployeeFunctionLink.employee_number == employee_number).delete()
            session.merge(EmployeeFunctionLink(employee_number = employee_number, employee_function=kwargs['function']))
        else:
            session.query(EmployeeFunctionLink).filter(EmployeeFunctionLink.employee_number == employee_number).delete()

    if kwargs.__contains__('programs'):
        if kwargs['programs']:
            try:
                session.query(EmployeeProgramLink).filter(EmployeeProgramLink.employee_number == employee_number).delete()
            except Exception as e:
                print(e)
            for pgm in kwargs['programs']:
                c_pgm = get_rows(Program, Program.id == pgm)
                session.merge(EmployeeProgramLink(employee_number=employee_number, employee_program=c_pgm[0].name))
                session.commit()
        else:
            session.query(EmployeeProgramLink).filter(EmployeeProgramLink.employee_number == employee_number).delete()

    if kwargs.__contains__('date_start') and kwargs['date_start']:
        employee.date_start = kwargs['date_start']

    if kwargs.__contains__('date_end'):
        if kwargs['date_end'] is None:
            employee.date_end = None
        else:
            employee.date_end = kwargs['date_end']

    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR: {e}')
        session.rollback()
        raise
    finally:
        session.close()


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
        app.logger.error('ERROR: Failed login with blank username at {}.'.format(log_time))
        return """Username can not be blank, please enter a username and try again."""

    if provided_password is None:
        app.logger.error('ERROR: Failed login with blank password using username {} at {}.'.format(username, log_time))
        return """Password can not be blank, please enter a password and try again."""
    if results is None:
        app.logger.error('ERROR: Failed login with username {} at {}, username not found'.format(username, log_time))
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
        app.logger.error('ERROR: Failed login with invalid password for username {} at {}'.format(username, log_time))
        return 'Invalid Password'
