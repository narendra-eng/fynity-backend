from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user, get_current_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middleware.role_required import role_required

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    role = (data.get("role") or "client").strip()

    if not full_name:
        return jsonify({"success": False, "message": "full_name is required."}), 400

    if not email:
        return jsonify({"success": False, "message": "email is required."}), 400

    if not password:
        return jsonify({"success": False, "message": "password is required."}), 400

    result = register_user(full_name, email, password, role)

    if not result["success"]:
        if result["message"] == "Email already registered.":
            return jsonify(result), 409
        return jsonify(result), 400

    return jsonify(result), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email:
        return jsonify({"success": False, "message": "email is required."}), 400

    if not password:
        return jsonify({"success": False, "message": "password is required."}), 400

    result = login_user(email, password)

    if not result["success"]:
        if result["message"] == "Account is inactive.":
            return jsonify(result), 403

        if result["message"] == "Invalid email or password.":
            return jsonify(result), 401

        return jsonify(result), 400

    return jsonify(result), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    return jsonify({
        "success": True,
        "message": "Protected route accessed successfully.",
        "user_id": user_id
    }), 200

@auth_bp.route("/admin", methods=["GET"])
@jwt_required()
@role_required("super_admin")
def admin_panel():
    return jsonify({
        "success": True,
        "message": "Welcome Super Admin"
    }), 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()

    result = get_current_user(user_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200