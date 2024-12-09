from flask import Blueprint, jsonify
from flask_login import login_required
from license_app.models import License

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/licenses', methods=['GET'])
@login_required
def get_licenses():
    licenses = License.query.all()
    return jsonify([{
        "id": license.id,
        "client_id": license.client_id,
        "license_key": license.license_key,
        "expires_at": license.expires_at,
        "max_ips": license.max_ips,
        "max_domains": license.max_domains,
        "license_term": license.license_term,
        "comment": license.comment
    } for license in licenses])