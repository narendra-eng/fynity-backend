from app.extensions import db
from app.models.company_settings import CompanySettings

def create_company_settings(
    company_name: str,
    email: str,
    phone: str,
    address: str = None,
    website: str = None,
    logo_url: str = None
) -> dict:

    settings = CompanySettings.query.first()

    if settings:
        return {
            "success": False,
            "message": "Company settings already exist."
        }

    settings = CompanySettings(
        company_name=company_name,
        email=email,
        phone=phone,
        address=address,
        website=website,
        logo_url=logo_url
    )

    try:
        db.session.add(settings)
        db.session.commit()

        return {
            "success": True,
            "message": "Company settings created successfully.",
            "company_settings": settings.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create company settings."
        }
    
def get_company_settings() -> dict:
    settings = CompanySettings.query.first()

    if not settings:
        return {
            "success": False,
            "message": "Company settings not found."
        }

    return {
        "success": True,
        "company_settings": settings.to_dict()
    }

def update_company_settings(data: dict) -> dict:
    settings = CompanySettings.query.first()

    if not settings:
        return {
            "success": False,
            "message": "Company settings not found."
        }

    if "company_name" in data:
        settings.company_name = data["company_name"]

    if "email" in data:
        settings.email = data["email"]

    if "phone" in data:
        settings.phone = data["phone"]

    if "address" in data:
        settings.address = data["address"]

    if "website" in data:
        settings.website = data["website"]

    if "logo_url" in data:
        settings.logo_url = data["logo_url"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Company settings updated successfully.",
            "company_settings": settings.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update company settings."
        }

def delete_company_settings() -> dict:
    settings = CompanySettings.query.first()

    if not settings:
        return {
            "success": False,
            "message": "Company settings not found."
        }

    try:
        db.session.delete(settings)
        db.session.commit()

        return {
            "success": True,
            "message": "Company settings deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete company settings."
        }    