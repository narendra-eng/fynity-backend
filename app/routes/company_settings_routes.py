from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.company_settings_service import (
    create_company_settings,
    get_company_settings,
    update_company_settings,
    delete_company_settings
)

company_settings_bp = Blueprint(
    "company_settings_bp",
    __name__
)

@company_settings_bp.route("/company-settings", methods=["POST"])
@jwt_required()
@role_required("super_admin")
def create_company_settings_route():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "company_name",
        "email",
        "phone"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_company_settings(
        company_name=data["company_name"],
        email=data["email"],
        phone=data["phone"],
        address=data.get("address"),
        website=data.get("website"),
        logo_url=data.get("logo_url")
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201