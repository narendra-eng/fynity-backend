from app.extensions import db
from app.models.workshop import Workshop
from datetime import datetime


def create_workshop(
    title: str,
    description: str,
    date: str,
    venue: str
) -> dict:

    workshop_date = datetime.strptime(date, "%Y-%m-%d").date()

    existing_workshop = Workshop.query.filter_by(
        title=title,
        date=workshop_date
    ).first()

    if existing_workshop:
        return {
            "success": False,
            "message": "Workshop already exists."
        }

    workshop = Workshop(
        title=title,
        description=description,
        date=workshop_date,
        venue=venue
    )

    try:
        db.session.add(workshop)
        db.session.commit()

        return {
            "success": True,
            "message": "Workshop created successfully.",
            "workshop": workshop.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create workshop."
        }
        
def get_all_workshops() -> dict:

    workshops = Workshop.query.all()

    return {
        "success": True,
        "count": len(workshops),
        "workshops": [
            workshop.to_dict() for workshop in workshops
        ]
    }
    
def get_workshop_by_id(workshop_id: str) -> dict:

    workshop = Workshop.query.get(workshop_id)

    if not workshop:
        return {
            "success": False,
            "message": "Workshop not found."
        }

    return {
        "success": True,
        "workshop": workshop.to_dict()
    }
    
def update_workshop(
    workshop_id: str,
    data: dict
) -> dict:

    workshop = Workshop.query.get(workshop_id)

    if not workshop:
        return {
            "success": False,
            "message": "Workshop not found."
        }

    if "title" in data:
        workshop.title = data["title"]

    if "description" in data:
        workshop.description = data["description"]

    if "date" in data:
        workshop.date = datetime.strptime(
            data["date"],
            "%Y-%m-%d"
        ).date()

    if "venue" in data:
        workshop.venue = data["venue"]

    if "status" in data:
        workshop.status = data["status"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Workshop updated successfully.",
            "workshop": workshop.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update workshop."
        }
        
def delete_workshop(workshop_id: str) -> dict:

    workshop = Workshop.query.get(workshop_id)

    if not workshop:
        return {
            "success": False,
            "message": "Workshop not found."
        }

    try:
        db.session.delete(workshop)
        db.session.commit()

        return {
            "success": True,
            "message": "Workshop deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete workshop."
        }
        
        