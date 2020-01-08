from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata

employee_function_association_table = Table('employee_function_mapping', metadata,
                                            Column('employee_number', Integer(), ForeignKey('employee_numbers.number')),
                                            Column('function_name', String(50), ForeignKey('functions.function')))

employee_project_association_table = Table('employee_project_mapping', metadata,
                                           Column('employee_number', Integer(), ForeignKey('employee_numbers.number')),
                                           Column('project_name', String(50), ForeignKey('projects.name')))


class EmployeeNumber(Base):
    __tablename__ = 'employee_numbers'

    id = Column(Integer(), primary_key=True)
    number = Column(Integer(), unique=True)

    # Registered User (One-to-One)
    registered_user = relationship('RegisteredUser', back_populates='employee_number', uselist=False)

    # Employee Data (One-to-Many)
    employee_data = relationship('EmployeeData', back_populates='employee_number')

    # Assigned Programs (One-to-Many)
    assigned_projects = relationship('ProjectData', secondary=employee_project_association_table,
                                     back_populates='employee_number')

    # Assigned Functions (Many-to-Many)
    assigned_functions = relationship('Functions', secondary=employee_function_association_table,
                                      back_populates='employees')
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

    # Department
    department = Column(String(50), ForeignKey('departments.department'))
    departments = relationship('Departments', back_populates='users')


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer(), primary_key=True)
    department = Column(String(50), nullable=False, unique=True, index=True)

    # Registered Users
    users = relationship('RegisteredUser', back_populates='departments', uselist=False)


class EmployeeData(Base):
    __tablename__ = 'employee_data'

    id = Column(Integer(), primary_key=True)
    name_last = Column(String(50), nullable=False, index=True)
    name_first = Column(String(50), nullable=False, index=True)
    job_title = Column(String(50), nullable=False)
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

    # Employee Numbers (Many-to-One)
    # employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_number = relationship('EmployeeNumber', secondary=employee_project_association_table,
                                   back_populates='assigned_projects')

    # Program (Many-to-One)
    program_name = Column(String(50), ForeignKey('programs.name'))
    program = relationship('Program', back_populates='project')

    # Usage Entry (One-to-Many)
    time_entry = relationship('ResourceUsage', back_populates='project')


class ChargeNumber(Base):
    __tablename__ = 'charge_numbers'

    id = Column(Integer(), primary_key=True)
    charge_number = Column(String(50), nullable=False, unique=True)

    # Project (One-to-One)
    project_name = Column(String(50), ForeignKey('projects.name'))
    project = relationship('ProjectData', back_populates='charge_number', uselist=False)


class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Projects (One-to-Many)
    project = relationship('ProjectData', back_populates='program')


class ResourceUsage(Base):
    __tablename__ = 'resource_entries'

    id = Column(Integer(), primary_key=True)
    year = Column(Integer(), nullable=False)
    period = Column(Integer(), nullable=False)
    sub_period = Column(Integer(), nullable=False)
    quarter = Column(Integer(), nullable=False)
    hours = Column(Numeric(3, 2), nullable=False)

    # Project (Many-to-One)
    project_name = Column(String(50), ForeignKey('projects.name'))
    project = relationship('ProjectData', back_populates='time_entry')

    # Employee Numbers (Many-to-One)
    employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_number = relationship('EmployeeNumber', back_populates='resource_entries')


class Functions(Base):
    __tablename__ = 'functions'

    id = Column(Integer(), primary_key=True)
    function = Column(String(50), unique=True, nullable=False, index=True)

    # One-to-Many relationships
    employees = relationship('EmployeeNumber', secondary=employee_function_association_table,
                             back_populates='assigned_functions')
