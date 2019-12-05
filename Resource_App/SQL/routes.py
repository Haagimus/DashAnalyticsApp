from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from database import SessionLocal, engine
from models import EmployeeNumber, Employee, FinanceFunction, RegisteredUser, \
    ChargeNumber, Program, Project, ResourceEntry


@app.route('/', methods=['GET'])
def create_user():
    username = request.args.get('user')
    employeeNumber = request.args.get('email')
    password = request.args.get('password')
    if username and employeeNumber:
        new_user = RegisteredUser(username=username,
                employeeNumber=employeeNumber,
                password=password)
        