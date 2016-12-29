from flask import Flask
from config import config
from flask_login import LoginManager
from .models import db, User
from .admin.views import flask_admin
from flask.ext.qrcode import QRcode

login_manager = LoginManager()
qrcode = QRcode()


def create_app(config_name):
    """Creates Flask app."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    flask_admin.init_app(app)
    login_manager.init_app(app)
    qrcode.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    return app
