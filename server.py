import os
import time

from dash import Dash
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import dash_bootstrap_components as dbc

db = SQLAlchemy()
login_manager = LoginManager()
log_time = time.strftime('%d%b%y %H:%M:%S')
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"


server = Flask(__name__)
app = Dash(__name__,
           server=server,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 FONT_AWESOME])
app.config.suppress_callback_exceptions = True
login_manager.init_app(server)
