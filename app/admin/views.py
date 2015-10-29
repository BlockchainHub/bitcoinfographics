from flask import redirect, url_for
from .. import flask_admin, db
import flask_admin as adm
from flask_admin import AdminIndexView, helpers, expose
from flask_admin.contrib.sqla import ModelView
from ..models import Infographic, User
import flask_login
from wtforms import fields, validators
from wtforms.form import Form
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask


class LoginForm(Form):

    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])


    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')
        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class MyModelView(ModelView):

    def is_accessible(self):
        return flask_login.current_user.is_authenticated


class MyAdminIndexView(adm.AdminIndexView):


    @expose('/')
    def index(self):
        form = LoginForm(request.form)
        if not flask_login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()


    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            flask_login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView, self).index()


    @expose('/logout/')
    def logout_view(self):
        flask_login.logout_user()
        return redirect(url_for('.index'))

flask_admin.add_view(MyModelView(Infographic, db.session))
