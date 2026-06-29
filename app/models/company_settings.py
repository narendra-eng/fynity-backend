from app.extensions import db
import uuid
from sqlalchemy.sql import func


class CompanySettings(db.Model):
    __tablename__ = "company_settings"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    company_name = db.Column(db.String(255), nullable=False)

    email = db.Column(db.String(255), nullable=False)

    phone = db.Column(db.String(20), nullable=False)

    address = db.Column(db.Text, nullable=True)

    website = db.Column(db.String(255), nullable=True)

    logo_url = db.Column(db.String(500), nullable=True)

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
            "company_name": self.company_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "website": self.website,
            "logo_url": self.logo_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }