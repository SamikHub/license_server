import os
import datetime
import jwt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Змінні середовища
DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql+psycopg2://myuser:mypassword@db:5432/licenses_db")
PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "/app/keys/private_key.pem")
PUBLIC_KEY_PATH = os.environ.get("PUBLIC_KEY_PATH", "/app/keys/public_key.pem")
ALGORITHM = "RS256"

# Ініціалізація застосунку
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "your_secret_key")

db = SQLAlchemy(app)

class License(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), nullable=False)
    license_key = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    features = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

# Ініціалізація Flask-Admin
admin = Admin(app, name='License Admin', template_mode='bootstrap4')
admin.add_view(ModelView(License, db.session))

# Завантаження ключів
with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()

@app.route("/license/create", methods=["POST"])
def create_license():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    client_id = data.get("client_id")
    if not client_id:
        return jsonify({"error": "Client ID is required"}), 400

    expiration_days = data.get("days", 30)
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days)
    features = data.get("features", [])

    payload = {
        "client_id": client_id,
        "exp": expiration_date,
        "issued_at": datetime.datetime.utcnow().isoformat(),
        "features": features
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

    # Зберігаємо в базу даних
    new_license = License(
        client_id=client_id,
        license_key=token,
        expires_at=expiration_date,
        features=",".join(features) if features else None
    )
    db.session.add(new_license)
    db.session.commit()

    return jsonify({"license_key": token}), 200

@app.route("/license/validate", methods=["POST"])
def validate_license():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    license_key = data.get("license_key")
    if not license_key:
        return jsonify({"error": "License key is required"}), 400

    try:
        decoded = jwt.decode(license_key, PUBLIC_KEY, algorithms=[ALGORITHM])
        # Додаткова перевірка за базою: чи існує ця ліцензія, чи не відкликана
        lic = License.query.filter_by(license_key=license_key).first()
        if not lic:
            return jsonify({"status": "invalid"}), 401

        # Перевіряємо термін дії:
        if lic.expires_at < datetime.datetime.utcnow():
            return jsonify({"status": "expired"}), 401

        return jsonify({"status": "valid", "payload": decoded}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"status": "expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "invalid"}), 401

if __name__ == "__main__":
    # Ініціалізація схеми БД при першому запуску
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000)