from app.extensions import db
import uuid
from sqlalchemy.sql import func


class Workshop(db.Model):
    __tablename__ = "workshops"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text, nullable=True)

    date = db.Column(db.Date, nullable=False)

    venue = db.Column(db.String(255), nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="upcoming"
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
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
            "venue": self.venue,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }