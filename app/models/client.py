from app.extensions import db
import uuid
from sqlalchemy.sql import func


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = db.Column(
        db.String(36),
        db.ForeignKey("users.id"),
        nullable=False
    )
    
    project_milestones = db.relationship(
        "ProjectMilestone",
        backref="client",
        lazy=True,
        cascade="all, delete-orphan"
    )
    invoices = db.relationship(
        "Invoice",
        backref="client",
        lazy=True,
        cascade="all, delete-orphan"
    )

    company_name = db.Column(db.String(255), nullable=False)

    contact_person = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(255), unique=True, nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    website = db.Column(db.String(255), nullable=True)

    address = db.Column(db.Text, nullable=True)

    industry = db.Column(db.String(100), nullable=True)

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
            "user_id": self.user_id,
            "company_name": self.company_name,
            "contact_person": self.contact_person,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
            "address": self.address,
            "industry": self.industry,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }