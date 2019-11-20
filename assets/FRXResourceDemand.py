# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, ForeignKey, Index, Integer, Numeric, String, text
from sqlalchemy.dialects.mssql import BIT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ChargeNumber(Base):
    __tablename__ = 'ChargeNumbers'

    Charge_Numbers = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class EmployeeDatum(Base):
    __tablename__ = 'EmployeeData'
    __table_args__ = (
        Index('KEY_Employees', 'Employee_Number', 'Assigned_Program', unique=True),
    )

    Name_Last = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Name_First = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Employee_Number = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Job_Title = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Level = Column(Numeric(8, 0))
    Function_Finance = Column(ForeignKey('Finance_Functions.Finance_Functions'))
    Job_Code = Column(String(6, 'SQL_Latin1_General_CP1_CI_AS'))
    Date_Start = Column(Date, nullable=False)
    Date_End = Column(Date)
    Name_Full = Column(String(102, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Assigned_Program = Column(ForeignKey('Programs.Program_Name'))
    IsAdmin = Column(BIT, nullable=False, server_default=text("((0))"))

    Program = relationship('Program')
    Finance_Function = relationship('FinanceFunction')


class EmployeeNumber(EmployeeDatum):
    __tablename__ = 'EmployeeNumbers'

    Employee_Number = Column(ForeignKey('EmployeeData.Employee_Number'), primary_key=True)


class FinanceFunction(Base):
    __tablename__ = 'Finance_Functions'

    Finance_Functions = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class HRFunction(Base):
    __tablename__ = 'HR_Functions'

    HR_Function = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)


class Program(Base):
    __tablename__ = 'Programs'

    Program_Name = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)
    Assigned_Employees = Column(ForeignKey('EmployeeNumbers.Employee_Number'))
    ChargeNumbers = Column(ForeignKey('ChargeNumbers.Charge_Numbers'))

    EmployeeNumber = relationship('EmployeeNumber')
    ChargeNumber = relationship('ChargeNumber')


class ProjectDatum(Base):
    __tablename__ = 'ProjectData'

    Date_Start = Column(Date)
    Date_End = Column(Date)
    Parent_Program = Column(ForeignKey('Programs.Program_Name'), nullable=False)
    Program_Type = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Project_Name = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True)

    Program = relationship('Program')


class RegisteredUser(Base):
    __tablename__ = 'RegisteredUsers'

    Username = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True, nullable=False)
    Password = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EmployeeNumber = Column(ForeignKey('EmployeeNumbers.Employee_Number'), primary_key=True, nullable=False)

    EmployeeNumber1 = relationship('EmployeeNumber')


class ResourceTable(Base):
    __tablename__ = 'ResourceTable'

    ID = Column(Integer, primary_key=True)
    Year = Column(Integer)
    Period = Column(Integer)
    SubPeriod = Column(Integer)
    Quarter = Column(Integer)
    Hours = Column(DECIMAL(1, 0))
    Employee_Number = Column(ForeignKey('EmployeeNumbers.Employee_Number'), nullable=False)
    Program_Name = Column(ForeignKey('Programs.Program_Name'), nullable=False)

    EmployeeNumber = relationship('EmployeeNumber')
    Program = relationship('Program')
