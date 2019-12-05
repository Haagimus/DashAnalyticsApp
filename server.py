from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash import Dash

__name__ = 'Resource and Analysis Website'

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/')
app.config.suppress_callback_exceptions = True
db = SQLAlchemy(server)
