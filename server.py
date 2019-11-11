from flask import Flask
from dash import Dash

server = Flask('Resource and Analysis Website')
app = Dash(server=server)
app.config.suppress_callback_exceptions = True
