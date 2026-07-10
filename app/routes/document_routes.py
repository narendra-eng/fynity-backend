from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.middleware.role_required import role_required

from app.services.document_service import (
    upload_document,
    get_all_documents,
    download_document,
    delete_document
)

document_bp = Blueprint(
    "document_bp",
    __name__
)


# -------------------------
# Upload Document
# -------------------------
@document_bp.route("/documents/upload", methods=["POST"])
@jwt_required()
@role_required("super_admin", "admin")
def upload_document_route():

    client_id = request.form.get("client_id")

    if not client_id:
        return jsonify({
            "success": False,
            "message": "client_id is required."
        }), 400

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": "File is required."
        }), 400

    file = request.files["file"]

    result = upload_document(
        client_id,
        file
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201


# -------------------------
# Get All Documents
# -------------------------
@document_bp.route("/documents", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def get_all_documents_route():

    result = get_all_documents()

    return jsonify(result), 200

@document_bp.route("/documents/<string:document_id>/download", methods=["GET"])
@jwt_required()
@role_required("super_admin", "admin")
def download_document_route(document_id):

    result = download_document(document_id)

    if isinstance(result, dict):
        return jsonify(result), 404

    return result

@document_bp.route("/documents/<string:document_id>", methods=["DELETE"])
@jwt_required()
@role_required("super_admin", "admin")
def delete_document_route(document_id):

    result = delete_document(document_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result), 200