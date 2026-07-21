from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required
from app.services.dashboard_service import get_dashboard_summary

dashboard_bp = Blueprint("dashboard_bp", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def dashboard_summary_route():
    result = get_dashboard_summary()
    return jsonify(result), 200