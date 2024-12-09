from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import db, License

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/licenses", methods=["GET"])
@login_required
def get_licenses():
    licenses = License.query.all()
    return jsonify([{
        "id": license.id,
        "client_id": license.client_id,
        "license_key": license.license_key,
        "expires_at": license.expires_at,
        "created_at": license.created_at,
        "max_ips": license.max_ips,
        "max_domains": license.max_domains,
        "comment": license.comment
    } for license in licenses]), 200

@admin_bp.route("/licenses", methods=["POST"])
@login_required
def create_license():
    data = request.json
    new_license = License(
        client_id=data.get("client_id"),
        license_key=data.get("license_key"),
        expires_at=data.get("expires_at"),
        max_ips=data.get("max_ips"),
        max_domains=data.get("max_domains"),
        comment=data.get("comment")
    )
    db.session.add(new_license)
    db.session.commit()
    return jsonify({"message": "License created"}), 201