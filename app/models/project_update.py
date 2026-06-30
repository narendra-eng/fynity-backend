from app.extensions import db
import uuid
from sqlalchemy.sql import func


class ProjectUpdate(db.Model):
    __tablename__ = "project_updates"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    milestone_id = db.Column(
        db.String(36),
        db.ForeignKey("project_milestones.id"),
        nullable=False
    )

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=False)

    update_date = db.Column(
        db.Date,
        nullable=False
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
            "milestone_id": self.milestone_id,
            "title": self.title,
            "description": self.description,
            "update_date": self.update_date.isoformat() if self.update_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }