from flask import Flask
from app.extensions import db, migrate, jwt
from app.config.config import Config
from app.models.workshop import Workshop
from app.models.mentorship_student import MentorshipStudent
from app.models.project_milestone import ProjectMilestone
from app.models.project_update import ProjectUpdate
from app.models.invoice import Invoice
from app.models.invoice_line_item import InvoiceLineItem

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.models.user import User
    from app.models.client import Client
    from app.models.company_settings import CompanySettings
    from app.models.college_partner import CollegePartner
    from app.routes.company_settings_routes import company_settings_bp
    from app.routes.college_partner_routes import college_partner_bp
    from app.routes.workshop_routes import workshop_bp
    from app.routes.mentorship_student_routes import mentorship_student_bp
    from app.routes.project_milestone_routes import project_milestone_bp
    from app.routes.project_update_routes import project_update_bp
    from app.routes.invoice_routes import invoice_bp
    from app.routes.invoice_line_item_routes import invoice_line_item_bp
    
    

    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.client_routes import client_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(company_settings_bp)
    app.register_blueprint(college_partner_bp)
    app.register_blueprint(workshop_bp)
    app.register_blueprint(mentorship_student_bp)
    app.register_blueprint(project_milestone_bp)
    app.register_blueprint(project_update_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(invoice_line_item_bp)

    return app