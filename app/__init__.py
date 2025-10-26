import os
from flask import Flask
from flask_login import LoginManager
from datetime import datetime

# Initialize extensions  
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///kolel_crm.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    from app.models import db
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'אנא התחבר למערכת'
    login_manager.login_message_category = 'info'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.avrech import bp as avrech_bp
    app.register_blueprint(avrech_bp, url_prefix='/avrech')
    
    from app.attendance import bp as attendance_bp
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    
    from app.payment_profiles import bp as payment_profiles_bp
    app.register_blueprint(payment_profiles_bp, url_prefix='/payment-profiles')
    
    from app.calendar import bp as calendar_bp
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    
    from app.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
    
    return app

from app import models