# coding: utf-8
from flask_login import UserMixin
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
metadata = Base.metadata


class EmployeeNumber(Base):
    __tablename__ = 'employee_numbers'

    id = Column(Integer(), primary_key=True)
    number = Column(Integer(), unique=True)

    registered_user_id = Column(Integer(), ForeignKey('registered_users.id'))
    registered_user = relationship('RegisteredUser', backref=backref('employee_numbers', uselist=False))

    # employee_data_id = Column(Integer(), ForeignKey('employee_data.id'))
    # employee_data = relationship('EmployeeData', backref=backref('employee_numbers', uselist=False))


class RegisteredUser(UserMixin, Base):
    __tablename__ = 'registered_users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(), nullable=False)
    employee_number = Column(Integer(), unique=True)

    # Foreign Keys
    department_id = Column(Integer(), ForeignKey('departments.id'))
    departments = relationship('Departments', backref=backref('registered_users'))

    # One-to-One relationships

    # Many-to-One relationship
    admin_of = relationship('Departments')


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer(), primary_key=True)
    department = Column(String(50), nullable=False, unique=True, index=True)

    # One-to-Many relationships
    users = relationship('RegisteredUser', back_populates='departments')


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

    # Foreign Keys
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    assigned_programs = Column(String(50), ForeignKey('programs.name'))
    assigned_function = Column(String(50), ForeignKey('functions.function'))

    # One-to-One relationships
    function = relationship('Functions', backref=backref('assigned_function'))
    number = relationship('EmployeeNumber', backref=backref('employee_number'))

    # One-to-Many relationships
    # number = relationship('EmployeeNumber', backref=backref('employee_data'))
    programs = relationship('Program', backref=backref('employee_data'))


class ChargeNumber(Base):
    __tablename__ = 'charge_numbers'

    id = Column(Integer(), primary_key=True)
    charge_number = Column(String(50), nullable=False, unique=True)


class Program(Base):
    __tablename__ = 'programs'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Foreign Keys
    employee_numbers = Column(Integer(), ForeignKey('employee_numbers.number'))
    charge_number = Column(String(50), ForeignKey('charge_numbers.charge_number'))
    entries = Column(Integer(), ForeignKey('resource_entries.id'))

    # One to One relationship
    charge = relationship('ChargeNumber', uselist=False)

    # One-to-Many relationships
    employees = relationship('EmployeeData', back_populates='programs')


class ProjectData(Base):
    __tablename__ = 'projects'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    date_start = Column(Date(), nullable=False)
    date_end = Column(Date(), nullable=True)
    program_type = Column(String(50), nullable=True)

    # Foreign Keys
    parent_program = Column(String(50), ForeignKey('programs.name'))

    # One-to-One relationships
    program = relationship('Program', uselist=False)

    # One-to-Many relationships
    time_entries = relationship('ResourceUsage', back_populates='projects')


class ResourceUsage(Base):
    __tablename__ = 'resource_entries'

    id = Column(Integer(), primary_key=True)
    year = Column(Integer(), nullable=False)
    period = Column(Integer(), nullable=False)
    sub_period = Column(Integer(), nullable=False)
    quarter = Column(Integer(), nullable=False)
    hours = Column(Numeric(3, 2), nullable=False)

    # Foreign Keys
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))
    project_id = Column(Integer(), ForeignKey('projects.id'))
    projects = relationship('ProjectData', backref=backref('resource_entries', uselist=False))

    # One-to-Many relationships
    number = relationship('EmployeeNumber', backref=backref('resource_entries'))


class Functions(Base):
    __tablename__ = 'functions'

    id = Column(Integer(), primary_key=True)
    function = Column(String(50), unique=True, nullable=False, index=True)

    # Foreign Keys
    employee_numbers = Column(Integer(), ForeignKey('employee_numbers.number'))

    # One-to-Many relationships
    employees = relationship('EmployeeData', backref=backref('functions'))

