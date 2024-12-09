from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('license_app.config.Config')

    # Ініціалізація розширень
    db.init_app(app)
    login_manager.init_app(app)

    # Імпорт та реєстрація Blueprint
    from license_app.auth import auth_bp
    from license_app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Ініціалізація бази даних
    with app.app_context():
        db.create_all()

    return app