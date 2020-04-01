import time

import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
log_time = time.strftime('%d%b%y %H:%M:%S')
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
card_style = {
    "box-shadow": "0 4px 5px 0 rgba(0,0,0,0.14), 0 1px 10px 0 rgba(0,0,0,0.12), 0 2px 4px -1px rgba(0,0,0,0.3)"
}
# TODO: move all style information to css file

server = Flask(__name__)
app = Dash(__name__,
           server=server,
           external_stylesheets=[dbc.themes.BOOTSTRAP,
                                 FONT_AWESOME])
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
login_manager.init_app(server)
