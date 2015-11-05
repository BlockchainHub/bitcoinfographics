import os
import os.path as op
import subprocess
import time
from flask import redirect, url_for, request, current_app, make_response
from flask.ext.admin import Admin
import flask_admin as admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask_admin import helpers, expose
import flask.ext.login as login
from wtforms.form import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import required, ValidationError
from werkzeug.security import check_password_hash
from ..models import Infographic, User
from ..models import db


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


class MyFileAdmin(FileAdmin):


    def is_accessible(self):
        return login.current_user.is_authenticated


class MyAdminIndexView(admin.AdminIndexView):


    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()


    @expose('/backup-db/')
    def backup_db(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
        db_filepath = db_uri[db_uri.find('sqlite:///')+10:]
        subprocess.call(['7z', 'a', '-p'+os.environ.get('ZIP_PASS'), 'db.7z', db_filepath])
        try:
            with open('db.7z', 'rb') as db_file:
                response = make_response(db_file.read())
                response.headers["Content-Disposition"] = "attachment; filename=bitcoinfographics_db-" + str(time.time()) + ".7z"
                return response
        except Exception:
            return("Oops! Call an administrator. :P")



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
        return redirect(url_for('main.index'))

flask_admin = Admin(name='bitcoinfographics',
                    index_view=MyAdminIndexView(),
                    base_template='my_master.html',
                    template_mode='bootstrap3')

flask_admin.add_view(MyModelView(Infographic, db.session))

path = op.join(op.dirname(__file__), '../static/img/infographics')
flask_admin.add_view(MyFileAdmin(path,
                                 '/static/img/infographics/',
                                  name='Infographic Files'))
