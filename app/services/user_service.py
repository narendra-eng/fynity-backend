from app.models.user import User
from app.extensions import db

def get_all_users() -> dict:
    users = User.query.all()

    return {
        "success": True,
        "count": len(users),
        "users": [user.to_dict() for user in users]
    }

def get_user_by_id(user_id: str) -> dict:
    user = User.query.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    return {
        "success": True,
        "user": user.to_dict()
    }

def update_user(user_id: str, data: dict) -> dict:
    user = User.query.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    if "full_name" in data:
        user.full_name = data["full_name"]

    if "role" in data:
        user.role = data["role"]

    if "is_active" in data:
        user.is_active = data["is_active"]

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "User updated successfully.",
            "user": user.to_dict()
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to update user."
        }
    
def delete_user(user_id: str) -> dict:
    user = User.query.get(user_id)

    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    user.is_active = False

    try:
        db.session.commit()

        return {
            "success": True,
            "message": "User deactivated successfully."
        }

    except Exception:
        db.session.rollback()

        return {
            "success": False,
            "message": "Failed to deactivate user."
        }