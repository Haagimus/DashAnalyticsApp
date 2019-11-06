from flask import Flask
from dash import Dash

server = Flask('Resources and Data Analysis')
app = Dash(server=server)
app.config.suppress_callback_exceptions = True
