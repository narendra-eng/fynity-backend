from app.extensions import db
from app.models.payment import Payment
from app.models.invoice import Invoice
from datetime import datetime


def update_invoice_status(invoice_id):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return

    total_paid = sum(payment.amount for payment in invoice.payments)

    if total_paid <= 0:
        invoice.status = "pending"

    elif total_paid < invoice.total_amount:
        invoice.status = "partially_paid"

    else:
        invoice.status = "paid"

    db.session.commit()


def create_payment(
    invoice_id,
    amount,
    payment_date,
    payment_method,
    reference_number=None,
    notes=None
):

    invoice = Invoice.query.get(invoice_id)

    if not invoice:
        return {
            "success": False,
            "message": "Invoice not found."
        }

    if amount <= 0:
        return {
            "success": False,
            "message": "Payment amount must be greater than zero."
        }

    total_paid = sum(payment.amount for payment in invoice.payments)

    if total_paid + amount > invoice.total_amount:
        return {
            "success": False,
            "message": "Payment exceeds invoice amount."
        }

    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        payment_date=datetime.strptime(
            payment_date,
            "%Y-%m-%d"
        ).date(),
        payment_method=payment_method,
        reference_number=reference_number,
        notes=notes
    )

    try:
        db.session.add(payment)
        db.session.commit()

        update_invoice_status(invoice_id)

        return {
            "success": True,
            "message": "Payment created successfully.",
            "payment": payment.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create payment."
        }


def get_all_payments():

    payments = Payment.query.all()

    return {
        "success": True,
        "count": len(payments),
        "payments": [
            payment.to_dict()
            for payment in payments
        ]
    }


def get_payment_by_id(payment_id):

    payment = Payment.query.get(payment_id)

    if not payment:
        return {
            "success": False,
            "message": "Payment not found."
        }

    return {
        "success": True,
        "payment": payment.to_dict()
    }


def update_payment(payment_id, data):

    payment = Payment.query.get(payment_id)

    if not payment:
        return {
            "success": False,
            "message": "Payment not found."
        }

    if "amount" in data:

        if data["amount"] <= 0:
            return {
                "success": False,
                "message": "Payment amount must be greater than zero."
            }

        payment.amount = data["amount"]

    if "payment_method" in data:
        payment.payment_method = data["payment_method"]

    if "reference_number" in data:
        payment.reference_number = data["reference_number"]

    if "notes" in data:
        payment.notes = data["notes"]

    if "payment_date" in data:
        payment.payment_date = datetime.strptime(
            data["payment_date"],
            "%Y-%m-%d"
        ).date()

    try:
        db.session.commit()

        update_invoice_status(payment.invoice_id)

        return {
            "success": True,
            "message": "Payment updated successfully.",
            "payment": payment.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update payment."
        }


def delete_payment(payment_id):

    payment = Payment.query.get(payment_id)

    if not payment:
        return {
            "success": False,
            "message": "Payment not found."
        }

    invoice_id = payment.invoice_id

    try:
        db.session.delete(payment)
        db.session.commit()

        update_invoice_status(invoice_id)

        return {
            "success": True,
            "message": "Payment deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete payment."
        }