from flask import Flask
from dash import Dash
from flask_sqlalchemy import SQLAlchemy

server = Flask('Resource and Analysis Website')
app = Dash(server=server)
db = SQLAlchemy()
app.config.suppress_callback_exceptions = True
