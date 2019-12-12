from dash import Dash
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
external_stylesheets = ['dbc.themes.BOOTSTRAP']

server = Flask('Resource and Analysis Website')
app = Dash(server=server, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
login_manager.init_app(server)

# TODO: Research [dcc.Store](https://dash.plot.ly/dash-core-components/store) for user caching, this will be used for admin
