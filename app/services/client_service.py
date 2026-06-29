from app.extensions import db
from app.models.client import Client

def create_client(
    user_id: str,
    company_name: str,
    contact_person: str,
    email: str,
    phone: str,
    website: str = None,
    address: str = None,
    industry: str = None
) -> dict:

    existing_client = Client.query.filter_by(email=email).first()

    if existing_client:
        return {
            "success": False,
            "message": "Client already exists."
        }

    client = Client(
        user_id=user_id,
        company_name=company_name,
        contact_person=contact_person,
        email=email,
        phone=phone,
        website=website,
        address=address,
        industry=industry
    )

    try:
        db.session.add(client)
        db.session.commit()

        return {
            "success": True,
            "message": "Client created successfully.",
            "client": client.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create client."
        }