from app.extensions import db
from app.models.client import Client
from app.services.audit_log_service import create_audit_log
from math import ceil
from sqlalchemy import or_
from sqlalchemy import or_, asc, desc

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
        
        create_audit_log(
        user_id=user_id,
        action="CREATE",
        module="CLIENT",
        description=f"Client '{company_name}' created."
    )

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
    
    
from sqlalchemy import or_

def get_all_clients(page=1, limit=10, search=None, sort=None):

    query = Client.query

    if search:
        query = query.filter(
            or_(
                Client.company_name.ilike(f"%{search}%"),
                Client.contact_person.ilike(f"%{search}%"),
                Client.email.ilike(f"%{search}%"),
                Client.industry.ilike(f"%{search}%")
            )
        )

    if sort:

        if sort.startswith("-"):
            field = sort[1:]

            if hasattr(Client, field):
                query = query.order_by(
                    desc(getattr(Client, field))
                )

        else:

            if hasattr(Client, sort):
                query = query.order_by(
                    asc(getattr(Client, sort))
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
        "clients": [
            client.to_dict()
            for client in pagination.items
        ]
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
    
def delete_client(client_id: str) -> dict:
    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    try:
        db.session.delete(client)
        db.session.commit()

        return {
            "success": True,
            "message": "Client deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete client."
        }