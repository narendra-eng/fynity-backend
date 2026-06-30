from app.extensions import db
import uuid
from sqlalchemy.sql import func


class MentorshipStudent(db.Model):
    __tablename__ = "mentorship_students"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    full_name = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(255), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    college = db.Column(db.String(255), nullable=False)

    course = db.Column(db.String(255), nullable=False)

    year = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "college": self.college,
            "course": self.course,
            "year": self.year,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }