import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False