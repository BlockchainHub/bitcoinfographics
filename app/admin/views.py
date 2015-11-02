from flask import render_template, redirect, url_for, request
import flask.ext.login as login
from flask.ext.login import login_user
from wtforms.form import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import required, ValidationError
from werkzeug.security import check_password_hash
from ..models import Infographic
import flask_admin as admin
from flask_admin import helpers, expose
from flask.ext.admin.contrib.sqla import ModelView
from ..models import db
from ..models import User
from flask.ext.admin import Admin


class LoginForm(Form):
    login = TextField(validators=[required()])
    password = PasswordField(validators=[required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class MyModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=['GET', 'POST'])
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()


    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

flask_admin = Admin(name='bitcoinfographics',
                    index_view=MyAdminIndexView(),
                    base_template='my_master.html',
                    template_mode='bootstrap3')

flask_admin.add_view(MyModelView(Infographic, db.session))
