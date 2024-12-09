from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
import pyotp
import qrcode
import io

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # У продакшні використовуйте хешування паролів!
        login_user(user)
        if user.twofa_enabled:
            session["2fa_verified"] = False
            return jsonify({"message": "2FA required"}), 200
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route("/2fa/setup", methods=["POST"])
@login_required
def setup_2fa():
    user = current_user
    if user.twofa_enabled:
        return jsonify({"error": "2FA already enabled"}), 400

    user.twofa_secret = pyotp.random_base32()
    db.session.commit()

    otp = pyotp.TOTP(user.twofa_secret)
    qr = qrcode.make(otp.provisioning_uri(user.username, issuer_name="License Server"))
    buf = io.BytesIO()
    qr.save(buf)
    buf.seek(0)
    return jsonify({"qr_code": buf.getvalue().hex()}), 200

@auth_bp.route("/2fa/verify", methods=["POST"])
@login_required
def verify_2fa():
    data = request.json
    token = data.get("token")

    otp = pyotp.TOTP(current_user.twofa_secret)
    if otp.verify(token):
        session["2fa_verified"] = True
        return jsonify({"message": "2FA verified"}), 200

    return jsonify({"error": "Invalid 2FA token"}), 401