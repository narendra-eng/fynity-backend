from app.extensions import db
from app.models.college_partner import CollegePartner

def create_college_partner(
    name: str,
    contact_person: str,
    email: str,
    phone: str,
    website: str = None,
    address: str = None
) -> dict:

    existing_partner = CollegePartner.query.filter_by(email=email).first()

    if existing_partner:
        return {
            "success": False,
            "message": "College partner already exists."
        }

    partner = CollegePartner(
        name=name,
        contact_person=contact_person,
        email=email,
        phone=phone,
        website=website,
        address=address
    )

    try:
        db.session.add(partner)
        db.session.commit()

        return {
            "success": True,
            "message": "College partner created successfully.",
            "college_partner": partner.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create college partner."
        }
        
        
        
def get_all_college_partners() -> dict:
    partners = CollegePartner.query.all()

    return {
        "success": True,
        "count": len(partners),
        "college_partners": [
            partner.to_dict() for partner in partners
        ]
    }
    
def get_college_partner_by_id(partner_id: str) -> dict:
    partner = CollegePartner.query.get(partner_id)

    if not partner:
        return {
            "success": False,
            "message": "College partner not found."
        }

    return {
        "success": True,
        "college_partner": partner.to_dict()
    }
    
    
def update_college_partner(
    partner_id: str,
    data: dict
) -> dict:

    partner = CollegePartner.query.get(partner_id)

    if not partner:
        return {
            "success": False,
            "message": "College partner not found."
        }

    if "name" in data:
        partner.name = data["name"]

    if "contact_person" in data:
        partner.contact_person = data["contact_person"]

    if "email" in data:
        partner.email = data["email"]

    if "phone" in data:
        partner.phone = data["phone"]

    if "website" in data:
        partner.website = data["website"]

    if "address" in data:
        partner.address = data["address"]

    if "status" in data:
        partner.status = data["status"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "College partner updated successfully.",
            "college_partner": partner.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update college partner."
        }
        
        
def delete_college_partner(partner_id: str) -> dict:
    partner = CollegePartner.query.get(partner_id)

    if not partner:
        return {
            "success": False,
            "message": "College partner not found."
        }

    try:
        db.session.delete(partner)
        db.session.commit()

        return {
            "success": True,
            "message": "College partner deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete college partner."
        }                