from . import db
from datetime import datetime


class Infographic(db.Model):
    """Infographic model."""
    __tablename__ = 'infographics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)
    download_url = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    """Admin users model."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
