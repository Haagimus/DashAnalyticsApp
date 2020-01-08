from dash import Dash
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
external_stylesheets = ['dbc.themes.BOOTSTRAP']

server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
login_manager.init_app(server)
