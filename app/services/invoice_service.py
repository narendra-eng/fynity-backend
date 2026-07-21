from app.extensions import db
from app.models.invoice import Invoice
from app.models.client import Client
from datetime import datetime
from sqlalchemy import or_, asc, desc


def create_invoice(
    client_id: str,
    invoice_number: str,
    issue_date: str,
    due_date: str,
    total_amount: float,
    notes: str = None
) -> dict:

    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    existing_invoice = Invoice.query.filter_by(
        invoice_number=invoice_number
    ).first()

    if existing_invoice:
        return {
            "success": False,
            "message": "Invoice number already exists."
        }

    issue = datetime.strptime(issue_date, "%Y-%m-%d").date()
    due = datetime.strptime(due_date, "%Y-%m-%d").date()

    if due < issue:
        return {
            "success": False,
            "message": "Due date cannot be earlier than issue date."
        }

    if total_amount <= 0:
        return {
            "success": False,
            "message": "Total amount must be greater than zero."
        }

    invoice = Invoice(
        client_id=client_id,
        invoice_number=invoice_number,
        issue_date=issue,
        due_date=due,
        total_amount=total_amount,
        notes=notes
    )

    try:
        db.session.add(invoice)
        db.session.commit()

        return {
            "success": True,
            "message": "Invoice created successfully.",
            "invoice": invoice.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create invoice."
        }


def get_all_invoices(
    page=1,
    limit=10,
    search=None,
    sort=None
):

    query = Invoice.query

    # Search
    if search:
        query = query.filter(
            or_(
                Invoice.invoice_number.ilike(f"%{search}%"),
                Invoice.status.ilike(f"%{search}%"),
                Invoice.notes.ilike(f"%{search}%")
            )
        )

    # Sorting
    if sort:

        if sort.startswith("-"):
            field = sort[1:]

            if hasattr(Invoice, field):
                query = query.order_by(
                    desc(getattr(Invoice, field))
                )

        else:

            if hasattr(Invoice, sort):
                query = query.order_by(
                    asc(getattr(Invoice, sort))
                )

    pagination = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )

    return {
        "success": True,
        "page": page,
        "limit": limit,
        "total": pagination.total,
        "total_pages": pagination.pages,
        "invoices": [
            invoice.to_dict()
            for invoice in pagination.items
        ]
    }


def get_invoice_by_id(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "success": False,
            "message": "Invoice not found."
        }

    return {
        "success": True,
        "invoice": invoice.to_dict()
    }


def update_invoice(invoice_id, data):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "success": False,
            "message": "Invoice not found."
        }

    if "issue_date" in data:
        invoice.issue_date = datetime.strptime(
            data["issue_date"],
            "%Y-%m-%d"
        ).date()

    if "due_date" in data:
        invoice.due_date = datetime.strptime(
            data["due_date"],
            "%Y-%m-%d"
        ).date()

    if invoice.due_date < invoice.issue_date:
        return {
            "success": False,
            "message": "Due date cannot be earlier than issue date."
        }

    if "total_amount" in data:

        if data["total_amount"] <= 0:
            return {
                "success": False,
                "message": "Total amount must be greater than zero."
            }

        invoice.total_amount = data["total_amount"]

    if "status" in data:

        allowed_status = [
            "pending",
            "partially_paid",
            "paid",
            "overdue"
        ]

        if data["status"] not in allowed_status:
            return {
                "success": False,
                "message": "Invalid invoice status."
            }

        invoice.status = data["status"]

    if "notes" in data:
        invoice.notes = data["notes"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Invoice updated successfully.",
            "invoice": invoice.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update invoice."
        }


def delete_invoice(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "success": False,
            "message": "Invoice not found."
        }

    try:
        db.session.delete(invoice)
        db.session.commit()

        return {
            "success": True,
            "message": "Invoice deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete invoice."
        }