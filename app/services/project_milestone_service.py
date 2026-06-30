from app.extensions import db
from app.models.project_milestone import ProjectMilestone
from app.models.client import Client
from datetime import datetime


def create_project_milestone(
    client_id: str,
    title: str,
    description: str,
    due_date: str
) -> dict:

    client = Client.query.get(client_id)

    if not client:
        return {
            "success": False,
            "message": "Client not found."
        }

    milestone = ProjectMilestone(
        client_id=client_id,
        title=title,
        description=description,
        due_date=datetime.strptime(
            due_date,
            "%Y-%m-%d"
        ).date()
    )

    try:
        db.session.add(milestone)
        db.session.commit()

        return {
            "success": True,
            "message": "Project milestone created successfully.",
            "project_milestone": milestone.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to create project milestone."
        }


def get_all_project_milestones():

    milestones = ProjectMilestone.query.all()

    return {
        "success": True,
        "count": len(milestones),
        "project_milestones": [
            milestone.to_dict()
            for milestone in milestones
        ]
    }


def get_project_milestone_by_id(milestone_id):

    milestone = ProjectMilestone.query.get(milestone_id)

    if not milestone:
        return {
            "success": False,
            "message": "Project milestone not found."
        }

    return {
        "success": True,
        "project_milestone": milestone.to_dict()
    }


def update_project_milestone(
    milestone_id,
    data
):

    milestone = ProjectMilestone.query.get(milestone_id)

    if not milestone:
        return {
            "success": False,
            "message": "Project milestone not found."
        }

    if "title" in data:
        milestone.title = data["title"]

    if "description" in data:
        milestone.description = data["description"]

    if "due_date" in data:
        milestone.due_date = datetime.strptime(
            data["due_date"],
            "%Y-%m-%d"
        ).date()

    if "status" in data:
        milestone.status = data["status"]

    if "progress" in data:
        milestone.progress = data["progress"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "Project milestone updated successfully.",
            "project_milestone": milestone.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update project milestone."
        }


def delete_project_milestone(milestone_id):

    milestone = ProjectMilestone.query.get(milestone_id)

    if not milestone:
        return {
            "success": False,
            "message": "Project milestone not found."
        }

    try:
        db.session.delete(milestone)
        db.session.commit()

        return {
            "success": True,
            "message": "Project milestone deleted successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to delete project milestone."
        }