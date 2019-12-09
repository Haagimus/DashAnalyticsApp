from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Construct core application"""
    app = Flask(__name__, instance_relative_config=False)

    # Application configuration
    app.config.from_object('config.Config')

    # Initialize plugings
    db.init_app(app)
    login_manager.init_app(app)

