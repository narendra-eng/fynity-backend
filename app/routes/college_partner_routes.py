from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.college_partner_service import (
    create_college_partner,
    get_all_college_partners,
    get_college_partner_by_id,
    update_college_partner,
    delete_college_partner
)

college_partner_bp = Blueprint(
    "college_partner_bp",
    __name__
)

@college_partner_bp.route("/college-partners", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_college_partner_route():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "name",
        "contact_person",
        "email",
        "phone"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_college_partner(
        name=data["name"],
        contact_person=data["contact_person"],
        email=data["email"],
        phone=data["phone"],
        website=data.get("website"),
        address=data.get("address")
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201

@college_partner_bp.route("/college-partners", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_college_partners_route():

    result = get_all_college_partners()

    return jsonify(result), 200
@college_partner_bp.route("/college-partners/<string:partner_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_college_partner_route(partner_id):

    result = get_college_partner_by_id(partner_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200

@college_partner_bp.route("/college-partners/<string:partner_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_college_partner_route(partner_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_college_partner(partner_id, data)

    if not result["success"]:
        if result["message"] == "College partner not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200

@college_partner_bp.route("/college-partners/<string:partner_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_college_partner_route(partner_id):

    result = delete_college_partner(partner_id)

    if not result["success"]:
        if result["message"] == "College partner not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200