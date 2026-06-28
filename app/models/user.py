# app/models/user.py

import uuid
from datetime import datetime, timezone
from app.extensions import db
import bcrypt


class User(db.Model):
    __tablename__ = "users"

    # Primary key as UUID — avoids sequential ID enumeration attacks
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Full name for display purposes
    full_name = db.Column(db.String(120), nullable=False)

    # Email is the unique login identifier
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # Never store raw passwords — only bcrypt hash
    password_hash = db.Column(db.String(255), nullable=False)

    # Role controls what this user can access (RBAC)
    role = db.Column(
    db.String(30),
    nullable=False,
    default="client"
    )

    # Soft delete / account suspension without removing the record
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Audit timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    clients = db.relationship(
    "Client",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
)

    # ── Helper methods ──────────────────────────────────────────────

    def set_password(self, plain_password: str) -> None:
        """Hash and store the password. Never call db.session.add here."""
        self.password_hash = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """Return True if the plain password matches the stored hash."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    def to_dict(self) -> dict:
        """Safe serialization — password_hash is intentionally excluded."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.email} | {self.role}>"