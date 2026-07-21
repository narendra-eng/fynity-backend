from app.extensions import db
import uuid
from sqlalchemy.sql import func


class ProjectMilestone(db.Model):
    __tablename__ = "project_milestones"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    client_id = db.Column(
        db.String(36),
        db.ForeignKey("clients.id"),
        nullable=False
    )

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    due_date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    progress = db.Column(
        db.Integer,
        default=0,
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
    
    project_updates = db.relationship(
        "ProjectUpdate",
        backref="project_milestone",
        lazy=True,
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }