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