from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata


class EmployeeNumber(Base):
    __tablename__ = 'employee_numbers'

    id = Column(Integer(), primary_key=True)
    number = Column(Integer(), unique=True)

    # Registered User (One-to-One)
    registered_user = relationship('RegisteredUser', back_populates='employee_number', uselist=False)

    # Employee Data (One-to-Many)
    employee_data = relationship('EmployeeData', back_populates='employee_number')

    # Assigned Programs (Many-to-Many)
    assigned_programs = relationship('Program', secondary='employee_program_link')

    # Assigned Functions (Many-to-Many)
    assigned_functions = relationship('Functions', secondary='employee_function_link')

    # Resource Entry (One-to-Many)
    resource_entries = relationship('ResourceUsage', back_populates='employee_number')


class RegisteredUser(Base):
    __tablename__ = 'registered_users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(), nullable=False)

    # Employee Number
    employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_number = relationship('EmployeeNumber', back_populates='registered_user')

    # Function
    function = Column(String(50), ForeignKey('functions.function'))
    functions = relationship('Functions', back_populates='users')


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer(), primary_key=True)
    department = Column(String(50), nullable=False, unique=True, index=True)


class EmployeeData(Base):
    __tablename__ = 'employee_data'

    id = Column(Integer(), primary_key=True)
    name_last = Column(String(50), nullable=False, index=True)
    name_first = Column(String(50), nullable=False, index=True)
    job_title = Column(String(50), nullable=True)
    level = Column(Integer(), nullable=True)
    job_code = Column(String(10), nullable=False)
    date_start = Column(Date(), nullable=False)
    date_end = Column(Date(), nullable=True)
    is_admin = Column(Boolean(), nullable=False, default=False)

    # Employee Numbers (Many-to-One)
    employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_number = relationship('EmployeeNumber', back_populates='employee_data')


class ProjectData(Base):
    __tablename__ = 'projects'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    date_start = Column(Date(), nullable=False)
    date_end = Column(Date(), nullable=True)
    program_type = Column(String(50), nullable=True)

    # Charge Number (One-to-One)
    charge_number = relationship('ChargeNumber', back_populates='project', uselist=False)

    # Program (Many-to-One)
    program_name = Column(String(50), ForeignKey('programs.name', ondelete='CASCADE', onupdate='CASCADE'))
    program = relationship('Program', back_populates='project')

    # Usage Entry (One-to-Many)
    time_entry = relationship('ResourceUsage', back_populates='project')


class ChargeNumber(Base):
    __tablename__ = 'charge_numbers'

    id = Column(Integer(), primary_key=True)
    charge_number = Column(String(50), nullable=False, unique=True)

    # Project (One-to-One)
    project_name = Column(String(50), ForeignKey('projects.name', ondelete='CASCADE', onupdate='CASCADE'))
    project = relationship('ProjectData', back_populates='charge_number', uselist=False)


class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    comments = Column(String(), nullable=True)

    # Projects (One-to-Many)
    project = relationship('ProjectData', back_populates='program')

    # Employee Numbers (Many-to-One)
    employees = relationship(EmployeeNumber, secondary='employee_program_link')


class ResourceUsage(Base):
    __tablename__ = 'resource_entries'

    id = Column(Integer(), primary_key=True)
    year = Column(Integer(), nullable=False)
    period = Column(Integer(), nullable=False)
    sub_period = Column(Integer(), nullable=False)
    quarter = Column(Integer(), nullable=False)
    hours = Column(Numeric(3, 2), nullable=False)

    # Project (Many-to-One)
    project_name = Column(String(50), ForeignKey('projects.name', ondelete='CASCADE', onupdate='CASCADE'))
    project = relationship('ProjectData', back_populates='time_entry')

    # Employee Numbers (Many-to-One)
    employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_number = relationship('EmployeeNumber', back_populates='resource_entries')


class Functions(Base):
    __tablename__ = 'functions'

    id = Column(Integer(), primary_key=True)
    function = Column(String(50), unique=True, nullable=False, index=True)
    finance_function = Column(String(50), unique=True, nullable=True, index=True)

    # Employees Assigned (Many-to-Many)
    employees = relationship(EmployeeNumber, secondary='employee_function_link')

    # Registered Users
    users = relationship('RegisteredUser', back_populates='functions', uselist=False)


# region association tables
class EmployeeFunctionLink(Base):
    __tablename__ = 'employee_function_link'

    # TODO: Add relationship to display the employee start and end dates here to speed up relational searches and comparisons
    id = Column(Integer(), primary_key=True)
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_function = Column(String(50), ForeignKey('functions.function', ondelete='CASCADE', onupdate='CASCADE'))

    number = relationship(EmployeeNumber, backref=backref('employee_func_assoc'))
    function = relationship(Functions, backref=backref('function_assoc'))


class EmployeeProgramLink(Base):
    __tablename__ = 'employee_program_link'

    id = Column(Integer(), primary_key=True)
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_program = Column(String(50), ForeignKey('programs.name', ondelete='CASCADE', onupdate='CASCADE'))

    number = relationship(EmployeeNumber, backref=backref('employee_pgm_assoc'))
    program = relationship(Program, backref=backref('program_assoc'))
# endregion
