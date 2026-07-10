from app.extensions import db
import uuid
from sqlalchemy.sql import func


class Document(db.Model):
    __tablename__ = "documents"

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

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    stored_file_name = db.Column(
        db.String(255),
        nullable=False
    )

    file_path = db.Column(
        db.String(500),
        nullable=False
    )

    file_type = db.Column(
        db.String(100),
        nullable=False
    )

    file_size = db.Column(
        db.Integer,
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "file_name": self.file_name,
            "stored_file_name": self.stored_file_name,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }