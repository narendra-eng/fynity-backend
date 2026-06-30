from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.project_update_service import (
    create_project_update,
    get_all_project_updates,
    get_project_update_by_id,
    update_project_update,
    delete_project_update
)

project_update_bp = Blueprint(
    "project_update_bp",
    __name__
)


# CREATE
@project_update_bp.route("/project-updates", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_project_update_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "milestone_id",
        "title",
        "description",
        "update_date"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_project_update(
        milestone_id=data["milestone_id"],
        title=data["title"],
        description=data["description"],
        update_date=data["update_date"]
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@project_update_bp.route("/project-updates", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_project_updates_route():

    return jsonify(get_all_project_updates()), 200


# GET BY ID
@project_update_bp.route("/project-updates/<string:update_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_project_update_route(update_id):

    result = get_project_update_by_id(update_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@project_update_bp.route("/project-updates/<string:update_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_project_update_route(update_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_project_update(update_id, data)

    if not result["success"]:
        if result["message"] == "Project update not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@project_update_bp.route("/project-updates/<string:update_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_project_update_route(update_id):

    result = delete_project_update(update_id)

    if not result["success"]:
        if result["message"] == "Project update not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200