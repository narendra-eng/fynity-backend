from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.workshop_service import (
    create_workshop,
    get_all_workshops,
    get_workshop_by_id,
    update_workshop,
    delete_workshop
)

workshop_bp = Blueprint(
    "workshop_bp",
    __name__
)
@workshop_bp.route("/workshops", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_workshop_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "title",
        "date",
        "venue"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_workshop(
        title=data["title"],
        description=data.get("description"),
        date=data["date"],
        venue=data["venue"]
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201 

@workshop_bp.route("/workshops", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_workshops_route():

    result = get_all_workshops()

    return jsonify(result), 200

@workshop_bp.route("/workshops/<string:workshop_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_workshop_route(workshop_id):

    result = get_workshop_by_id(workshop_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200

@workshop_bp.route("/workshops/<string:workshop_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_workshop_route(workshop_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_workshop(workshop_id, data)

    if not result["success"]:
        if result["message"] == "Workshop not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200

@workshop_bp.route("/workshops/<string:workshop_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_workshop_route(workshop_id):

    result = delete_workshop(workshop_id)

    if not result["success"]:
        if result["message"] == "Workshop not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200