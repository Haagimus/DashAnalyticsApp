from flask import Flask
from dash import Dash
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

server = Flask('Resource and Analysis Website')
app = Dash(server=server)
app.config.suppress_callback_exceptions = True
login_manager.init_app(server)
