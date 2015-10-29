from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask_login import LoginManager

db = SQLAlchemy()
flask_admin = Admin(name='bitcoinfographics', template_mode='bootstrap3')
login_manager = LoginManager()

def create_app(config_name):
    """Creates Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    flask_admin.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
