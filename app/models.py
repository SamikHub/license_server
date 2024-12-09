from . import db

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    valid = db.Column(db.Boolean, default=True)