from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Ініціалізація базових об'єктів
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://myuser:mypassword@db:5432/licenses_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "your_secret_key"

    # Ініціалізація модулів
    db.init_app(app)
    login_manager.init_app(app)

    # Реєстрація Blueprint'ів
    from app.auth import auth_bp
    from app.admin import admin_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app