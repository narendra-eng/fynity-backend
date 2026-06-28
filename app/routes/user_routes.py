from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_users():
    result = get_all_users()
    return jsonify(result), 200

@user_bp.route("/users/<string:user_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_user(user_id):
    result = get_user_by_id(user_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200

@user_bp.route("/users/<string:user_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_user_route(user_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_user(user_id, data)

    if not result["success"]:
        if result["message"] == "User not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200

@user_bp.route("/users/<string:user_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_user_route(user_id):
    result = delete_user(user_id)

    if not result["success"]:
        if result["message"] == "User not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200