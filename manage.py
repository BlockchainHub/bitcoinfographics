#!/usr/bin/env python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import Infographic, User
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash
from flask.ext.assets import Environment, Bundle

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
assets = Environment(app)

if os.getenv('FLASK_CONFIG') == 'production':
    css = Bundle('components/normalize/normalize.css', 'css/foundation.css', 
                 'css/main.css', filters='cssmin', output='all.min.css')
    assets.register('css_all', css)
else:
    css = Bundle('components/normalize/normalize.css', 'css/foundation.css',
                 'css/main.css')
    assets.register('css_all', css)


def make_shell_context():
    return dict(app=app, db=db, Infographic=Infographic, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def mock_db():
    """ Create development/test db records."""
    user = User(login='test', password=generate_password_hash('test'))
    db.session.add(user)
    infographics_list = []
    try:
        for fn in os.listdir('./app/static/img/infographics/thumbnails'):
            if fn.endswith('.png'):
                infographics_list.append(fn.split('_')[0])
        for infographic_i in set(infographics_list):
            infographic_slug = infographic_i
            infographic_title = infographic_slug.replace('-', ' ')
            infographic = Infographic(title=infographic_title, slug=infographic_slug)
            db.session.add(infographic)
    except:
        print("No infographics found.")
    db.session.commit()


@manager.command
def test(coverage=False):
    """Run unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

if __name__ == '__main__':
    manager.run()
