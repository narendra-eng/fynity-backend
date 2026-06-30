from app.extensions import db
from app.models.project_update import ProjectUpdate
from app.models.project_milestone import ProjectMilestone
from datetime import datetime


def create_project_update(
    milestone_id: str,
    title: str,
    description: str,
    update_date: str
) -> dict:

    milestone = ProjectMilestone.query.get(milestone_id)

    if not milestone:
        return {
            "success": False,
            "message": "Project milestone not found."
        }

    project_update = ProjectUpdate(
        milestone_id=milestone_id,
        title=title,
        description=description,
        update_date=datetime.strptime(
            update_date,
            "%Y-%m-%d"
        ).date()
    )

    try:
        db.session.add(project_update)
        db.session.commit()

        return {
            "success": True,
            "message": "Project update created successfully.",
            "project_update": project_update.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create project update."
        }


def get_all_project_updates():

    updates = ProjectUpdate.query.all()

    return {
        "success": True,
        "count": len(updates),
        "project_updates": [
            update.to_dict()
            for update in updates
        ]
    }


def get_project_update_by_id(update_id):

    update = ProjectUpdate.query.get(update_id)

    if not update:
        return {
            "success": False,
            "message": "Project update not found."
        }

    return {
        "success": True,
        "project_update": update.to_dict()
    }


def update_project_update(update_id, data):

    update = ProjectUpdate.query.get(update_id)

    if not update:
        return {
            "success": False,
            "message": "Project update not found."
        }

    if "title" in data:
        update.title = data["title"]

    if "description" in data:
        update.description = data["description"]

    if "update_date" in data:
        update.update_date = datetime.strptime(
            data["update_date"],
            "%Y-%m-%d"
        ).date()

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Project update updated successfully.",
            "project_update": update.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update project update."
        }


def delete_project_update(update_id):

    update = ProjectUpdate.query.get(update_id)

    if not update:
        return {
            "success": False,
            "message": "Project update not found."
        }

    try:
        db.session.delete(update)
        db.session.commit()

        return {
            "success": True,
            "message": "Project update deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete project update."
        }