from app.extensions import db
from app.models.audit_log import AuditLog


def create_audit_log(
    user_id,
    action,
    module,
    description
):

    log = AuditLog(
        user_id=user_id,
        action=action,
        module=module,
        description=description
    )

    try:
        db.session.add(log)
        db.session.commit()

    except Exception:
        db.session.rollback()