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
    
    
def get_all_clients() -> dict:
    clients = Client.query.all()

    return {
        "success": True,
        "count": len(clients),
        "clients": [client.to_dict() for client in clients]
    }
    

def get_client_by_id(client_id: str) -> dict:
    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    return {
        "success": True,
        "client": client.to_dict()
    }

def update_client(client_id: str, data: dict) -> dict:
    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    if "company_name" in data:
        client.company_name = data["company_name"]

    if "contact_person" in data:
        client.contact_person = data["contact_person"]

    if "email" in data:
        client.email = data["email"]

    if "phone" in data:
        client.phone = data["phone"]

    if "website" in data:
        client.website = data["website"]

    if "address" in data:
        client.address = data["address"]

    if "industry" in data:
        client.industry = data["industry"]

    if "status" in data:
        client.status = data["status"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Client updated successfully.",
            "client": client.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update client."
        }