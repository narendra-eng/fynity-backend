from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.payment_service import (
    create_payment,
    get_all_payments,
    get_payment_by_id,
    update_payment,
    delete_payment
)

payment_bp = Blueprint(
    "payment_bp",
    __name__
)


# CREATE
@payment_bp.route("/payments", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_payment_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "invoice_id",
        "amount",
        "payment_date",
        "payment_method"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_payment(
        invoice_id=data["invoice_id"],
        amount=data["amount"],
        payment_date=data["payment_date"],
        payment_method=data["payment_method"],
        reference_number=data.get("reference_number"),
        notes=data.get("notes")
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@payment_bp.route("/payments", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_payments_route():

    return jsonify(get_all_payments()), 200


# GET BY ID
@payment_bp.route("/payments/<string:payment_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_payment_route(payment_id):

    result = get_payment_by_id(payment_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@payment_bp.route("/payments/<string:payment_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_payment_route(payment_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_payment(payment_id, data)

    if not result["success"]:
        if result["message"] == "Payment not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@payment_bp.route("/payments/<string:payment_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_payment_route(payment_id):

    result = delete_payment(payment_id)

    if not result["success"]:
        if result["message"] == "Payment not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200