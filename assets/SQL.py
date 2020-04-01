import binascii
import hashlib
import os

from sqlalchemy import create_engine, MetaData, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import BinaryExpression

import run
from assets.models import RegisteredUser, EmployeeData, Functions, Program, EmployeeNumber, EmployeeFunctionLink, \
    EmployeeProgramLink, ProjectData, ChargeNumber, ProgramProjectLink
from server import app, log_time

if run.args.localdb == 'True':
    dbname = 'Haag_Test'
else:
    dbname = 'FRXResourceDemand'

server = ''
driver = 'driver=SQL+Server'
t_conn = 'trusted_connections=yes'
MARS = 'MARS_Connection=No'
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


def get_rows(class_name, filter_text=None, distinct=None):
    """
    Returns all rows from selected columns in a table
    :param class_name: str
    :param filter_text: str
    :param distinct: bool
    :return: list[]
    """
    session.rollback()
    if filter_text is None:
        if distinct:
            results = session.query(class_name).distinct().all()
        else:
            results = session.query(class_name).all()
    elif type(filter_text) == dict:
        query = session.query(class_name)
        for attr, value in filter_text.items():
            if value == '':
                pass
            else:
                query = query.filter(getattr(class_name, attr) == value)
        if distinct:
            results = query.distinct().all()
        else:
            results = query.all()
    elif type(filter_text) == BinaryExpression:
        if distinct:
            results = session.query(class_name).filter(filter_text).distinct().all()
        else:
            results = session.query(class_name).filter(filter_text).all()
    else:
        if distinct:
            results = session.query(class_name).filter(filter_text).distinct().all()
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
    """
    empnum = session.query(EmployeeNumber).filter(EmployeeNumber.id == emp_num).first()
    query = EmployeeFunctionLink.employee_number == empnum.number
    func = get_rows(EmployeeFunctionLink, query)

    submission = RegisteredUser(username=username, employee_number=empnum, function=func[0].employee_function,
                                password=password)
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
    """
    number = (EmployeeNumber(number=employee_number))

    try:
        session.add(number)
        session.commit()
    except Exception as e:
        if 'Cannot insert duplicate key' in e.args[0]:
            app.logger.error(
                f'ERROR :: Add Employee Failed :: {employee_number} already exists in the table EmployeeNumber.')
        session.rollback()
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
            app.logger.error(f'ERROR :: [{e.orig.args[0]}] :: {e.orig.args[1]}')
            session.rollback()
            raise
        finally:
            session.close()

    employee = EmployeeData(name_first=first_name, name_last=last_name, employee_number_number=employee_number,
                            job_code=job_code,
                            level=level, date_start=start_date, date_end=end_date)
    try:
        session.add(employee)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: [{e.orig.args[0]}] :: {e.orig.args[1]}')
        session.rollback()
        raise
    finally:
        session.close()


def add_time_entry_df(dataframe):
    """
    Adds the dataframe passed to the resource_entities table overwriting existing entries with the new values
    :param dataframe: dataframe
    """
    # dataframe.to_sql(name='resource_entries_temp', con=conn, schema='dbo', if_exists='replace', chunksize=1000)

    # assuming we have already changed values in the rows and saved those changed rows in a separate DF: `x`
    x = dataframe  # `mask` should help us to find changed rows...

    # make sure `x` DF has a Primary Key column as index
    # x = x.set_index('uid')

    # dump a slice with changed rows to temporary MySQL table
    x.to_sql(name='resource_entries_temp', con=conn, if_exists='replace', index=False, dtype={'uid': String()})

    trans = conn.begin()

    try:
        # delete those rows that we are going to "upsert"
        engine.execute('delete from resource_entries where uid in (select uid from resource_entries_temp)')
        trans.commit()

        # insert changed rows
        x.to_sql('resource_entries', con=conn, if_exists='append', index=False, dtype={'uid': String()})
    except:
        trans.rollback()
        raise


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
            session.merge(EmployeeFunctionLink(employee_number=employee_number, employee_function=kwargs['function']))
        else:
            session.query(EmployeeFunctionLink).filter(EmployeeFunctionLink.employee_number == employee_number).delete()

    if kwargs.__contains__('programs'):
        if kwargs['programs']:
            try:
                session.rollback()
                session.query(EmployeeProgramLink).filter(
                    EmployeeProgramLink.employee_number == employee_number).delete()
                session.commit()
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

    if kwargs.__contains__('is_admin'):
        employee.is_admin = kwargs['is_admin']

    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
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
        app.logger.error('ERROR :: Failed login with blank username at {}.'.format(log_time))
        return """Username can not be blank, please enter a username and try again."""

    if provided_password is None:
        app.logger.error(
            'ERROR :: Failed login with blank password using username {} at {}.'.format(username, log_time))
        return """Password can not be blank, please enter a password and try again."""
    if results is None:
        app.logger.error('ERROR :: Failed login with username {} at {}, username not found'.format(username, log_time))
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
        app.logger.error('ERROR :: Failed login with invalid password for username {} at {}'.format(username, log_time))
        return 'Invalid Password'


def remove_duplicates(source_list):
    """
    :param source_list: []
    :return: List with duplicate values/objects removed
    """
    results = []
    for i in source_list:
        match = False
        for j in results:
            if i.id == j.id:
                match = True
        if not match:
            results.append(i)

    return results


def get_counts(date_filter):
    # TODO: Update this sql query to return a dataframe instead of filtering in the query, it can be done faster with
    #  a local dataframe
    count = {}
    # employees = get_rows(EmployeeData)
    employees = session.query(EmployeeData, EmployeeFunctionLink) \
        .filter(EmployeeData.employee_number_number == EmployeeFunctionLink.employee_number).all()
    # func_link_list = session.query(EmployeeFunctionLink).all()
    # test = session.query(EmployeeNumber).join(EmployeeData).all()
    ended = []
    active_employees = []

    for row in employees:
        if row.EmployeeData.date_start < date_filter and (
                row.EmployeeData.date_end is None or row.EmployeeData.date_end > date_filter):
            active_employees.append(row)
        if row.EmployeeData.date_end is not None:
            ended.append(row)

    func_list = [x.function for x in [f for f in get_rows(Functions)] if x.finance_function is not None]
    emp_func_list = [f.EmployeeFunctionLink.employee_function for f in active_employees]
    for i in func_list:
        count[i] = emp_func_list.count(i)
    count.update({'Total': len(active_employees)})

    return count


def add_charge_code(charge_number):
    session.rollback()
    new_chg = ChargeNumber(charge_number=charge_number)
    try:
        session.add(new_chg)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def add_project_data(chg_id, proj_name, maj_prog, prog_type, date_start, date_end=None):
    """
    Update a project and associated information
    :keyword chg_id: str
    :keyword proj_name: str
    :keyword maj_prog: Program
    :keyword prog_type: str
    :keyword date_start: date
    :keyword date_end: date
    """
    session.rollback()
    charge = get_rows(ChargeNumber, ChargeNumber.id == chg_id)[0]
    new_proj = ProjectData(charge_number=charge, name=proj_name, date_start=date_start,
                           date_end=date_end, program_type=prog_type)

    try:
        session.add(new_proj)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()

    if maj_prog is not None:
        session.merge(ProgramProjectLink(program_name=maj_prog, project_name=proj_name))

    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()

    session.close()


def add_function(func_entry, fin_func_entry):
    """
    Update a function entry
    :param func_entry: str
    :param fin_func_entry: str
    """
    new_func = Functions(function=func_entry, finance_function=fin_func_entry)
    try:
        session.add(new_func)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def add_program(prog_name, prog_comments=None, projects=None, employees=None):
    """
    Update a function entry
    :param prog_name: str
    :param prog_comments: str
    :param projects: [Program.name(str), ProjectData.name(str)]
    :param employees: [EmployeeNumber.number(int), Program.name(str)]
    """
    new_prog = Program(name=prog_name, comments=prog_comments)

    try:
        session.add(new_prog)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()

    if projects is not None:
        queries = []
        for p in projects:
            queries.append(ProgramProjectLink.insert().values(program_name=new_prog.name, project_name=p))

    if employees is not None:
        queries = [] if queries is None else queries
        for e in employees:
            queries.append(EmployeeProgramLink.insert().values(program_name=new_prog.name, employee_number=e))

        for q in queries:
            try:
                session.execute(q)
                session.commit()
            except Exception as e:
                app.logger.error(f'ERROR :: {e}')
                session.rollback()

    session.close()


def update_charge_code(chg_id, charge_code_entry):
    """
    Update a function name or finance function
    :param charge_code_entry: str
    """
    session.rollback()

    charge = get_rows(ChargeNumber, ChargeNumber.id == chg_id)

    charge[0].charge_number = charge_code_entry
    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def update_project_data(chg_id, **kwargs):
    """
    Update a project and associated information
    :keyword charge_number: str
    :keyword project_name: str
    :keyword major_program: Program
    :keyword program_type: str
    :keyword project_date_start: date
    :keyword project_date_end: date
    """
    session.rollback()

    charge = get_rows(ChargeNumber, ChargeNumber.id == chg_id)[0]
    project = session.query(ProjectData).filter(ProjectData.charge_number == charge).first()

    if kwargs.__contains__('project_name'):
        if kwargs['project_name']:
            project.name = kwargs['project_name']
        else:
            project.name = 'not entered'

    if kwargs.__contains__('major_program'):
        if kwargs['major_program']:
            project.program_name = kwargs['major_program']
        else:
            project.program_name = None

        if kwargs.__contains__('program_type'):
            if kwargs['program_type']:
                project.program_type = kwargs['program_type']
            else:
                project.program_type = None

    if kwargs.__contains__('project_date_start') and kwargs['project_date_start']:
        project.date_start = kwargs['project_date_start']

    if kwargs.__contains__('project_date_end'):
        if kwargs['project_date_end'] is None:
            project.date_end = None
        else:
            project.date_end = kwargs['project_date_end']

    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def update_function(func_entry, fin_func_entry, func_id=None):
    """
    Update a function name or finance function
    :param func_entry: str
    :param fin_func_entry: str
    :param func_id: int
    """
    session.rollback()

    func = get_rows(Functions, Functions.id == func_id)

    func[0].function = func_entry
    func[0].finance_function = fin_func_entry
    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def update_program(prog_id, **kwargs):
    """
    Update a program and associated information
    :keyword prog_id: int
    :keyword program_name: str
    :keyword program_comments: Program
    :keyword projects: [Program.name(str), ProjectData.name(str)]
    :keyword employees: [EmployeeNumber.number(int), Program.name(str)]
    """
    session.rollback()

    pgm = get_rows(Program, Program.id == prog_id)[0]

    if kwargs.__contains__('program_name'):
        if kwargs['program_name']:
            pgm.name = kwargs['program_name']
        else:
            pgm.name = None

    if kwargs.__contains__('program_comments'):
        if kwargs['program_comments']:
            pgm.comments = kwargs['program_comments']
        else:
            pgm.comments = None

    if kwargs.__contains__('projects'):
        if kwargs['projects']:
            try:
                session.query(ProgramProjectLink).filter(
                    ProgramProjectLink.program_name == pgm.name).delete()
                session.commit()
            except Exception as e:
                print(e)
            for proj in kwargs['projects']:
                c_proj = get_rows(ProjectData, ProjectData.id == proj)
                session.merge(ProgramProjectLink(program_name=pgm.name, project_name=c_proj[0].name))
                session.commit()
        else:
            session.query(ProgramProjectLink).filter(ProgramProjectLink.program_name == pgm.namw).delete()

    if kwargs.__contains__('employees'):
        if kwargs['employees']:
            try:
                session.query(EmployeeProgramLink).filter(
                    EmployeeProgramLink.employee_program == pgm.name).delete()
                session.commit()
            except Exception as e:
                print(e)
            for emp in kwargs['employees']:
                c_emp = get_rows(EmployeeNumber, EmployeeNumber.number == emp)
                session.merge(EmployeeProgramLink(employee_number=c_emp[0].number, employee_program=pgm.name))
                session.commit()
        else:
            session.query(EmployeeProgramLink).filter(EmployeeProgramLink.program == pgm.name).delete()

    try:
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def delete_project_data(proj_id):
    """
    Delete a project
    :keyword proj_id: int
    """
    session.rollback()
    proj = get_rows(ProjectData, ProjectData.id == proj_id)[0]
    session.query(ProgramProjectLink).filter(ProgramProjectLink.project_name == proj.name).delete()

    try:
        session.delete(proj)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def delete_charge_code(chg_id):
    """
    Delete a project
    :keyword chg_id: int
    """
    session.rollback()
    chg = get_rows(ChargeNumber, ChargeNumber.id == chg_id)[0]

    try:
        session.delete(chg)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def delete_function(func_id):
    """
    Delete a project
    :keyword func_id: int
    """
    session.rollback()
    func = get_rows(Functions, Functions.id == func_id)[0]

    try:
        session.delete(func)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()


def delete_program(prog_id):
    """
    Delete a project
    :keyword prog_id: int
    """
    session.rollback()
    prog = get_rows(Program, Program.id == prog_id)[0]
    session.query(ProgramProjectLink).filter(ProgramProjectLink.program_name == prog.name).delete()

    try:
        session.delete(prog)
        session.commit()
    except Exception as e:
        app.logger.error(f'ERROR :: {e}')
        session.rollback()
    finally:
        session.close()

