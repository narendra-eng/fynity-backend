from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.invoice_service import (
    create_invoice,
    get_all_invoices,
    get_invoice_by_id,
    update_invoice,
    delete_invoice
)

invoice_bp = Blueprint(
    "invoice_bp",
    __name__
)


# CREATE
@invoice_bp.route("/invoices", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_invoice_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "client_id",
        "invoice_number",
        "issue_date",
        "due_date",
        "total_amount"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_invoice(
        client_id=data["client_id"],
        invoice_number=data["invoice_number"],
        issue_date=data["issue_date"],
        due_date=data["due_date"],
        total_amount=data["total_amount"],
        notes=data.get("notes")
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@invoice_bp.route("/invoices", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_invoices_route():

    return jsonify(get_all_invoices()), 200


# GET BY ID
@invoice_bp.route("/invoices/<string:invoice_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_invoice_route(invoice_id):

    result = get_invoice_by_id(invoice_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@invoice_bp.route("/invoices/<string:invoice_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_invoice_route(invoice_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_invoice(invoice_id, data)

    if not result["success"]:
        if result["message"] == "Invoice not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@invoice_bp.route("/invoices/<string:invoice_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_invoice_route(invoice_id):

    result = delete_invoice(invoice_id)

    if not result["success"]:
        if result["message"] == "Invoice not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200