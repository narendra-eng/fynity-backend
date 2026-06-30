from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.mentorship_student_service import (
    create_mentorship_student,
    get_all_mentorship_students,
    get_mentorship_student_by_id,
    update_mentorship_student,
    delete_mentorship_student
)

mentorship_student_bp = Blueprint(
    "mentorship_student_bp",
    __name__
)


# CREATE
@mentorship_student_bp.route("/mentorship-students", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_mentorship_student_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "full_name",
        "email",
        "phone",
        "college",
        "course",
        "year"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_mentorship_student(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        college=data["college"],
        course=data["course"],
        year=data["year"]
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@mentorship_student_bp.route("/mentorship-students", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_mentorship_students_route():

    result = get_all_mentorship_students()

    return jsonify(result), 200


# GET BY ID
@mentorship_student_bp.route("/mentorship-students/<string:student_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_mentorship_student_route(student_id):

    result = get_mentorship_student_by_id(student_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@mentorship_student_bp.route("/mentorship-students/<string:student_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_mentorship_student_route(student_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_mentorship_student(student_id, data)

    if not result["success"]:
        if result["message"] == "Mentorship student not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@mentorship_student_bp.route("/mentorship-students/<string:student_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_mentorship_student_route(student_id):

    result = delete_mentorship_student(student_id)

    if not result["success"]:
        if result["message"] == "Mentorship student not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200