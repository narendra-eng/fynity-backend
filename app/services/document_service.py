import os
import uuid

from flask import current_app, send_file
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.client import Client
from app.models.document import Document


ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "jpg",
    "jpeg",
    "png"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def upload_document(client_id, file):

    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    if not file or file.filename == "":
        return {
            "success": False,
            "message": "No file selected."
        }

    if not allowed_file(file.filename):
        return {
            "success": False,
            "message": "Invalid file type."
        }

    original_filename = secure_filename(file.filename)

    extension = original_filename.rsplit(".", 1)[1].lower()

    stored_filename = f"{uuid.uuid4()}.{extension}"

    upload_folder = os.path.abspath(
        os.path.join(
            current_app.root_path,
            "..",
            current_app.config["UPLOAD_FOLDER"]
        )
    )

    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        stored_filename
    )

    file.save(file_path)

    document = Document(
        client_id=client_id,
        file_name=original_filename,
        stored_file_name=stored_filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=os.path.getsize(file_path)
    )

    try:

        db.session.add(document)
        db.session.commit()

        return {
            "success": True,
            "message": "Document uploaded successfully.",
            "document": document.to_dict()
        }

    except Exception:

        db.session.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "success": False,
            "message": "Failed to upload document."
        }


def get_all_documents():

    documents = Document.query.all()

    return {
        "success": True,
        "count": len(documents),
        "documents": [
            document.to_dict()
            for document in documents
        ]
    }


def download_document(document_id):

    document = Document.query.get(document_id)

    if not document:
        return {
            "success": False,
            "message": "Document not found."
        }

    if not os.path.exists(document.file_path):
        return {
            "success": False,
            "message": "File not found on disk."
        }

    return send_file(
        document.file_path,
        as_attachment=True,
        download_name=document.file_name
    )
    
def delete_document(document_id):

    document = Document.query.get(document_id)

    if not document:
        return {
            "success": False,
            "message": "Document not found."
        }

    try:

        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        db.session.delete(document)
        db.session.commit()

        return {
            "success": True,
            "message": "Document deleted successfully."
        }

    except Exception:

        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete document."
        }