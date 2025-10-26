import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app, db
from app.models import User, Avrech, Branch, PaymentProfile, AttendanceLog, SystemCalendar, BonusRule

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Avrech': Avrech, 
        'Branch': Branch,
        'PaymentProfile': PaymentProfile,
        'AttendanceLog': AttendanceLog,
        'SystemCalendar': SystemCalendar,
        'BonusRule': BonusRule
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables and sample data"""
    db.create_all()
    
    # Create admin user if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@kolel.com',
            full_name='מנהל מערכת',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create sample branch
    branch = Branch.query.filter_by(name='כולל ראשי').first()
    if not branch:
        branch = Branch(
            name='כולל ראשי',
            address='רחוב הרב קוק 10, ירושלים',
            phone='02-1234567'
        )
        db.session.add(branch)
    
    # Create sample payment profile
    profile = PaymentProfile.query.filter_by(name='מסלול רגיל').first()
    if not profile:
        from datetime import time
        profile = PaymentProfile(
            name='מסלול רגיל',
            default_entry_time=time(8, 0),
            default_exit_time=time(13, 0),
            payment_method='daily_fixed',
            daily_amount=150.0,
            enable_late_penalty=True,
            late_penalty_method='fixed_amount',
            late_penalty_amount=10.0,
            late_penalty_interval=15,
            enable_absence_penalty=True,
            absence_penalty_method='full_day'
        )
        db.session.add(profile)
        db.session.flush()  # Get the ID
        
        # Add taanit dibur bonus
        bonus = BonusRule(
            payment_profile_id=profile.id,
            name='תענית דיבור',
            bonus_type='daily',
            amount=10.0,
            description='בונוס יומי עבור שמירת תענית דיבור'
        )
        db.session.add(bonus)
    
    db.session.commit()
    print("Database initialized successfully!")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='127.0.0.1', port=port)