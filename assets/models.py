from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata


class EmployeeNumber(Base):
    __tablename__ = 'employee_numbers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    number = Column(Integer(), unique=True)

    # Registered User (One-to-One)
    registered_user = relationship('RegisteredUser', back_populates='employee_number', uselist=False)

    # Employee Data (One-to-Many)
    employee_data = relationship('EmployeeData', lazy='dynamic', back_populates='employee_number')

    # Assigned Programs (Many-to-Many)
    assigned_programs = relationship('Program', lazy='dynamic', secondary='employee_program_link')

    # Assigned Functions (Many-to-Many)
    assigned_functions = relationship('Functions', lazy='dynamic', secondary='employee_function_link')

    # Resource Entry (One-to-Many)
    resource_entries = relationship('ResourceUsage', lazy='dynamic', back_populates='employee_number')


class RegisteredUser(Base):
    __tablename__ = 'registered_users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
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

    id = Column(Integer(), primary_key=True, autoincrement=True)
    department = Column(String(50), nullable=False, unique=True, index=True)


class EmployeeData(Base):
    __tablename__ = 'employee_data'

    id = Column(Integer(), primary_key=True, autoincrement=True)
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

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    date_start = Column(Date(), nullable=False)
    date_end = Column(Date(), nullable=True)
    program_type = Column(String(50), nullable=True)

    # Charge Number (One-to-One)
    charge_number = relationship('ChargeNumber', back_populates='project', uselist=False)

    # Program (Many-to-One)
    # program_name = Column(String(50), ForeignKey('programs.name', ondelete='CASCADE', onupdate='CASCADE'))
    # program = relationship('Program', back_populates='projects')
    programs = relationship('Program', lazy='dynamic', secondary='program_project_link')


class ChargeNumber(Base):
    __tablename__ = 'charge_numbers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    charge_number = Column(String(50), nullable=False, unique=True)

    # Project (One-to-One)
    project_name = Column(String(50), ForeignKey('projects.name', ondelete='CASCADE', onupdate='CASCADE'))
    project = relationship('ProjectData', back_populates='charge_number', uselist=False)

    # Usage Entry (One-to-Many)
    time_entry = relationship('ResourceUsage', lazy='dynamic', back_populates='charge')


class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, onupdate='CASCADE')
    comments = Column(String(), nullable=True)

    # Employee Numbers (Many-to-One)
    projects = relationship(ProjectData, secondary='program_project_link')
    employees = relationship(EmployeeNumber, secondary='employee_program_link')


class ResourceUsage(Base):
    __tablename__ = 'resource_entries'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    uid = Column(String(50), nullable=False)
    year = Column(Integer(), nullable=False)
    period = Column(Integer(), nullable=False)
    sub_period = Column(Integer(), nullable=False)
    quarter = Column(Integer(), nullable=False)
    month = Column(String(6), nullable=False)
    hours = Column(DECIMAL(precision=2), nullable=False)

    # Project (Many-to-One)
    charge_number = Column(String(50), ForeignKey('charge_numbers.charge_number', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    charge = relationship('ChargeNumber', back_populates='time_entry')

    # Employee Numbers (Many-to-One)
    employee_number_number = Column(Integer(), ForeignKey('employee_numbers.number'), nullable=True)
    employee_number = relationship('EmployeeNumber', back_populates='resource_entries')

    # Function (Many-to-One)
    function_name = Column(String(50), ForeignKey('functions.function'), nullable=False)
    function = relationship('Functions', back_populates='time_entry')

    def to_dict(self):
        return {
            'function': self.function_name,
            'charge': self.charge_number,
            'employee': self.employee_number_number,
            'year': self.year,
            'period': self.period,
            'sub-pd': self.sub_period,
            'quarter': self.quarter,
            'month': self.month,
            'hours': self.hours
        }


class Functions(Base):
    __tablename__ = 'functions'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    function = Column(String(50), unique=True, nullable=False, index=True)
    finance_function = Column(String(50), unique=True, nullable=True, index=True)

    # Employees Assigned (Many-to-Many)
    employees = relationship(EmployeeNumber, lazy='dynamic', secondary='employee_function_link')

    # Registered Users
    users = relationship('RegisteredUser', back_populates='functions', uselist=False)

    # Usage Entry (One-to-Many)
    time_entry = relationship('ResourceUsage', lazy='dynamic', back_populates='function')


# region association tables
class EmployeeFunctionLink(Base):
    __tablename__ = 'employee_function_link'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_function = Column(String(50), ForeignKey('functions.function', ondelete='CASCADE', onupdate='CASCADE'))

    number = relationship(EmployeeNumber, backref=backref('employee_func_assoc', lazy='dynamic'))
    function = relationship(Functions, backref=backref('function_assoc', lazy='dynamic'))


class EmployeeProgramLink(Base):
    __tablename__ = 'employee_program_link'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    employee_program = Column(String(50), ForeignKey('programs.name', ondelete='CASCADE', onupdate='CASCADE'))

    number = relationship(EmployeeNumber, backref=backref('employee_pgm_assoc', lazy='dynamic'))
    program = relationship(Program, backref=backref('program_assoc', lazy='dynamic'))


class ProgramProjectLink(Base):
    __tablename__ = 'program_project_link'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    program_name = Column(String(50), ForeignKey('programs.name', ondelete='CASCADE', onupdate='CASCADE'))
    project_name = Column(String(50), ForeignKey('projects.name', ondelete='CASCADE', onupdate='CASCADE'))

    program = relationship(Program, backref=backref('pgm_assoc', lazy='dynamic'))
    project = relationship(ProjectData, backref=backref('proj_assoc', lazy='dynamic'))

# endregion
