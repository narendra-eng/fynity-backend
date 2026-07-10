from app.models.client import Client
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.workshop import Workshop
from app.models.mentorship_student import MentorshipStudent


def get_dashboard_summary():

    total_clients = Client.query.count()

    total_invoices = Invoice.query.count()

    total_paid_invoices = Invoice.query.filter_by(
        status="paid"
    ).count()

    total_pending_invoices = Invoice.query.filter_by(
        status="pending"
    ).count()

    total_partially_paid = Invoice.query.filter_by(
        status="partially_paid"
    ).count()

    total_revenue = sum(
        invoice.total_amount
        for invoice in Invoice.query.filter_by(status="paid").all()
    )

    total_received = sum(
        payment.amount
        for payment in Payment.query.all()
    )

    outstanding_amount = sum(
        invoice.total_amount
        for invoice in Invoice.query.all()
    ) - total_received

    total_workshops = Workshop.query.count()

    total_students = MentorshipStudent.query.count()

    return {
        "success": True,
        "dashboard": {
            "total_clients": total_clients,
            "total_invoices": total_invoices,
            "paid_invoices": total_paid_invoices,
            "pending_invoices": total_pending_invoices,
            "partially_paid_invoices": total_partially_paid,
            "total_revenue": total_revenue,
            "total_received": total_received,
            "outstanding_amount": outstanding_amount,
            "total_workshops": total_workshops,
            "total_students": total_students
        }
    }