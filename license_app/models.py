from license_app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    twofa_enabled = db.Column(db.Boolean, default=False)
    twofa_secret = db.Column(db.String(32), nullable=True)

    licenses = db.relationship('License', backref='user', lazy=True)

class License(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), nullable=False)
    license_key = db.Column(db.String(128), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    max_ips = db.Column(db.Integer, nullable=False, default=1)
    max_domains = db.Column(db.Integer, nullable=False, default=1)
    license_term = db.Column(db.String(16), nullable=False, default='lifetime')
    comment = db.Column(db.Text, nullable=True)