from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.project_milestone_service import (
    create_project_milestone,
    get_all_project_milestones,
    get_project_milestone_by_id,
    update_project_milestone,
    delete_project_milestone
)

project_milestone_bp = Blueprint(
    "project_milestone_bp",
    __name__
)


# CREATE
@project_milestone_bp.route("/project-milestones", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_project_milestone_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "client_id",
        "title",
        "due_date"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_project_milestone(
        client_id=data["client_id"],
        title=data["title"],
        description=data.get("description"),
        due_date=data["due_date"]
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@project_milestone_bp.route("/project-milestones", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_project_milestones_route():

    return jsonify(get_all_project_milestones()), 200


# GET BY ID
@project_milestone_bp.route("/project-milestones/<string:milestone_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_project_milestone_route(milestone_id):

    result = get_project_milestone_by_id(milestone_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@project_milestone_bp.route("/project-milestones/<string:milestone_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_project_milestone_route(milestone_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_project_milestone(
        milestone_id,
        data
    )

    if not result["success"]:
        if result["message"] == "Project milestone not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@project_milestone_bp.route("/project-milestones/<string:milestone_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_project_milestone_route(milestone_id):

    result = delete_project_milestone(milestone_id)

    if not result["success"]:
        if result["message"] == "Project milestone not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200