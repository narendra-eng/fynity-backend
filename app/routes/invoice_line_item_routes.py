from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.invoice_line_item_service import (
    create_invoice_line_item,
    get_all_invoice_line_items,
    get_invoice_line_item_by_id,
    update_invoice_line_item,
    delete_invoice_line_item
)

invoice_line_item_bp = Blueprint(
    "invoice_line_item_bp",
    __name__
)


# CREATE
@invoice_line_item_bp.route("/invoice-line-items", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def create_invoice_line_item_route():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    required_fields = [
        "invoice_id",
        "description",
        "quantity",
        "unit_price"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    result = create_invoice_line_item(
        invoice_id=data["invoice_id"],
        description=data["description"],
        quantity=data["quantity"],
        unit_price=data["unit_price"]
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# GET ALL
@invoice_line_item_bp.route("/invoice-line-items", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_invoice_line_items_route():

    return jsonify(get_all_invoice_line_items()), 200


# GET BY ID
@invoice_line_item_bp.route("/invoice-line-items/<string:item_id>", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_invoice_line_item_route(item_id):

    result = get_invoice_line_item_by_id(item_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200


# UPDATE
@invoice_line_item_bp.route("/invoice-line-items/<string:item_id>", methods=["PUT"])
@jwt_required()
@role_required("super_admin", "admin")
def update_invoice_line_item_route(item_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body must be JSON."
        }), 400

    result = update_invoice_line_item(item_id, data)

    if not result["success"]:
        if result["message"] == "Invoice line item not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200


# DELETE
@invoice_line_item_bp.route("/invoice-line-items/<string:item_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_invoice_line_item_route(item_id):

    result = delete_invoice_line_item(item_id)

    if not result["success"]:
        if result["message"] == "Invoice line item not found.":
            return jsonify(result), 404

        return jsonify(result), 400

    return jsonify(result), 200