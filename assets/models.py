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


class RegisteredUser(UserMixin, Base):
    __tablename__ = 'registered_users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(), nullable=False)

    # Foreign Keys
    employee_number = Column(Integer(), ForeignKey('employee_numbers.number'))

    # One to One relationships
    employee = relationship('EmployeeNumber', uselist=False)


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

    # One to One relationships
    function = relationship('Functions', backref=backref('assigned_function'))

    # One to Many relationships
    number = relationship('EmployeeNumber', backref=backref('employee_data'))
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

    # One to Many relationships
    employees = relationship('EmployeeData', back_populates='programs')
    time_entries = relationship('ResourceUsage', back_populates='programs')


class ProjectData(Base):
    __tablename__ = 'projects'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    date_start = Column(Date(), nullable=False)
    date_end = Column(Date(), nullable=True)
    program_type = Column(String(50), nullable=True)

    # Foreign Keys
    parent_program = Column(String(50), ForeignKey('programs.name'))

    # One to One relationships
    program = relationship('Program', uselist=False)


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
    project = Column(String(50), ForeignKey('projects.name'))

    # One to Many relationships
    number = relationship('EmployeeNumber', backref=backref('resource_entries'))
    programs = relationship('Program', backref=backref('resource_entries'))


class Functions(Base):
    __tablename__ = 'functions'

    id = Column(Integer(), primary_key=True)
    function = Column(String(50), unique=True, nullable=False, index=True)

    # Foreign Keys
    employee_numbers = Column(Integer(), ForeignKey('employee_numbers.number'))

    # One to Many relationships
    employees = relationship('EmployeeData', backref=backref('functions'))
