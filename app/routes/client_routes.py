from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required
from app.services.client_service import (
    create_client,
    get_all_clients,
    get_client_by_id,
    update_client
)

client_bp = Blueprint("client_bp", __name__)

@client_bp.route("/clients", methods=["POST"])
@jwt_required()
@role_required("super_admin")
def create_client_route():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "user_id",
        "company_name",
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

    result = create_client(
        user_id=data["user_id"],
        company_name=data["company_name"],
        contact_person=data["contact_person"],
        email=data["email"],
        phone=data["phone"],
        website=data.get("website"),
        address=data.get("address"),
        industry=data.get("industry")
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201

@client_bp.route("/clients", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_clients():
    result = get_all_clients()
    return jsonify(result), 200

@client_bp.route("/clients/<string:client_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_client(client_id):
    result = get_client_by_id(client_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200

@client_bp.route("/clients/<string:client_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_client_route(client_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_client(client_id, data)

    if not result["success"]:
        if result["message"] == "Client not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200