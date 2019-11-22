from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from database import Base


class EmployeeNumber(Base):
    __table__ = 'EmployeeNumbers'

    EmployeeNumber = Column(Integer, primary_key=True, index=True)

    Employee = relationship('Employees', back_populates='EmployeeNumbers')
    RegisteredUsers = relationship('RegisteredUsers', back_populates='EmployeeNumbers')


class Employee(Base):
    __table__ = 'Employees'

    entryID = Column(Integer, primary_key=True, index=True)
    EmployeeNumber = Column(Integer, ForeignKey('EmployeeNumbers.EmployeeNumber'))
    NameLast = Column(String, nullable=False)
    NameFirst = Column(String, nullable=False)
    JobTitle = Column(String, nullable=True)
    Level = Column(Integer, nullable=True)
    FunctionFinance = Column(String, ForeignKey('FinanceFunctions.Function'), nullable=True)
    JobCode = Column(String, nullable=False)
    DateState = Column(Date, nullable=False)
    DateEnd = Column(Date, nullable=True)
    Assigned_Programs = Column(String, ForeignKey('Programs.ProgramName'), nullable=True)
    IsAdmin = Column(Boolean, nullable=False, default=False)

    Number = relationship('EmployeeNumbers', back_populates='Employees')
    FinanceFunctions = relationship('FinanceFunctions', back_populates='Employees')


class FinanceFunction(Base):
    __table__ = 'FinanceFunctions'

    Function = Column(String, primary_key=True, index=True)

    Employees = relationship('Employees', back_populates='FinanceFunctions')


class RegisteredUser(Base):
    __table__ = 'RegisteredUsers'

    Username = Column(String, primary_key=True, index=True)
    EmployeeNumber = Column(Integer, ForeignKey('EmployeeNumbers.EmployeeNumber'), nullable=False)
    Password = Column(String, nullable=False)

    Employees = relationship('Employees', back_populates='RegisteredUsers')


class ChargeNumber(Base):
    __table__ = 'ChargeNumbers'

    ChargeNumber = Column(String, primary_key=True, index=True)

    Program = relationship('Programs', back_populates='ChargeNumbers')


class Program(Base):
    __table__ = 'Programs'

    ProgramName = Column(String, primary_key=True, index=True)
    AssignedEmployees = Column(Integer, ForeignKey('EmployeeNumbers.EmployeeNumber'), nullable=True)
    ChargeNumbers = Column(String, ForeignKey('ChargeNumbers.ChargeNumber'), nullable=True)

    Employees = relationship('Employees', back_populates='Programs')
    Charges = relationship('ChargeNumbers', back_populates='Programs')


class Project(Base):
    __table__ = 'Projects'

    ProjectName = Column(String, primary_key=True, index=True)
    DateStart = Column(Date, nullable=True)
    DateEnd = Column(Date, nullable=True)
    ParentProgram = Column(String, ForeignKey('Programs.ProgramName'), nullable=False)
    ProgramType = Column(String, nullable=True)

    Program = relationship('Progams', back_populates='Projects')


class ResourceEntry(Base):
    __table__ = 'ResourceEntries'

    id = Columns(Integer, primary_key=True, index=True)
    Year = Column(Integer, nullable=False)
    Period = Column(Integer, nullable=False)
    SubPeriod = Column(Integer, nullable=False)
    Quarter = Column(Integer, nullable=False)
    Hours = Column(Float, nullable=False)
    Employee = Column(Integer, ForeignKey('EmployeeNumbers.EmployeeNumber'), nullable=False)
    Project = Column(String, ForeignKey('Projects.ProjectName'), nullable=False)

    EmployeeNumber = relationship('EmployeeNumbers', back_populates='ResourceEntries')
    ProjectName = relationship('Projects', back_populates='ResourceEntries')
