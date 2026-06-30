from app.extensions import db
from app.models.invoice import Invoice
from app.models.invoice_line_item import InvoiceLineItem


def update_invoice_total(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return

    total = 0

    for item in invoice.line_items:
        total += item.total_price

    invoice.total_amount = total

    db.session.commit()


def create_invoice_line_item(
    invoice_id,
    description,
    quantity,
    unit_price
):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "success": False,
            "message": "Invoice not found."
        }

    if quantity <= 0:
        return {
            "success": False,
            "message": "Quantity must be greater than zero."
        }

    if unit_price <= 0:
        return {
            "success": False,
            "message": "Unit price must be greater than zero."
        }

    total_price = quantity * unit_price

    item = InvoiceLineItem(
        invoice_id=invoice_id,
        description=description,
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price
    )

    try:
        db.session.add(item)
        db.session.commit()

        update_invoice_total(invoice_id)

        return {
            "success": True,
            "message": "Invoice line item created successfully.",
            "invoice_line_item": item.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create invoice line item."
        }


def get_all_invoice_line_items():

    items = InvoiceLineItem.query.all()

    return {
        "success": True,
        "count": len(items),
        "invoice_line_items": [
            item.to_dict() for item in items
        ]
    }


def get_invoice_line_item_by_id(item_id):

    item = InvoiceLineItem.query.get(item_id)

    if not item:
        return {
            "success": False,
            "message": "Invoice line item not found."
        }

    return {
        "success": True,
        "invoice_line_item": item.to_dict()
    }


def update_invoice_line_item(item_id, data):

    item = InvoiceLineItem.query.get(item_id)

    if not item:
        return {
            "success": False,
            "message": "Invoice line item not found."
        }

    if "description" in data:
        item.description = data["description"]

    if "quantity" in data:
        item.quantity = data["quantity"]

    if "unit_price" in data:
        item.unit_price = data["unit_price"]

    item.total_price = item.quantity * item.unit_price

    try:
        db.session.commit()

        update_invoice_total(item.invoice_id)

        return {
            "success": True,
            "message": "Invoice line item updated successfully.",
            "invoice_line_item": item.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update invoice line item."
        }


def delete_invoice_line_item(item_id):

    item = InvoiceLineItem.query.get(item_id)

    if not item:
        return {
            "success": False,
            "message": "Invoice line item not found."
        }

    invoice_id = item.invoice_id

    try:
        db.session.delete(item)
        db.session.commit()

        update_invoice_total(invoice_id)

        return {
            "success": True,
            "message": "Invoice line item deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete invoice line item."
        }