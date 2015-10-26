from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    """Creates Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
