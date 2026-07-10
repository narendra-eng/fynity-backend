import uuid
from datetime import datetime, timezone
from app.extensions import db
import bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    
    full_name = db.Column(db.String(120), nullable=False)

    
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

   
    password_hash = db.Column(db.String(255), nullable=False)

    
    role = db.Column(
        db.String(30),
        nullable=False,
        default="client"
    )

    
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    
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

    
    audit_logs = db.relationship(
        "AuditLog",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    
    def set_password(self, plain_password: str) -> None:
        """Hash and store the password."""
        self.password_hash = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        """Verify password."""
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            self.password_hash.encode("utf-8")
        )

    def to_dict(self) -> dict:
        """Safe serialization."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def __repr__(self) -> str:
        return f"<User {self.email} | {self.role}>"