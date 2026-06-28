from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token


def register_user(full_name: str, email: str, password: str, role: str = "client") -> dict:
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"success": False, "message": "Email already registered."}

    new_user = User(
        full_name=full_name,
        email=email,
        role=role
    )

    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return {
            "success": True,
            "message": "User registered successfully.",
            "user": new_user.to_dict()
        }
    except Exception:
        db.session.rollback()
        return {
            "success": False,
            "message": "Failed to register user."
        }

def login_user(email: str, password: str) -> dict:
    try:
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {
                "success": False,
                "message": "Invalid email or password."
            }

        if not user.is_active:
            return {
                "success": False,
                "message": "Account is inactive."
            }

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "role": user.role
            }
        )

        return {
            "success": True,
            "message": "Login successful.",
            "access_token": access_token,
            "user": user.to_dict()
        }

    except Exception:
        db.session.rollback()
        return {
            "success": False,
            "message": "Login failed."
        }
    
def get_current_user(user_id: str) -> dict:
    try:
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

    except Exception:
        return {
            "success": False,
            "message": "Failed to fetch user."
        }