#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
אתחול בסיס הנתונים למערכת CRM כוללים
"""

import os
import sys
from datetime import time

# הוספת התיקייה הנוכחית לpath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, Branch, PaymentProfile, BonusRule

def init_database():
    """אתחול בסיס הנתונים עם נתונים בסיסיים"""
    app = create_app()
    
    with app.app_context():
        print("יוצר טבלאות בסיס נתונים...")
        db.create_all()
        
        # בדיקה אם כבר יש משתמש admin
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("יוצר משתמש מנהל...")
            admin = User(
                username='admin',
                email='admin@kolel.com',
                full_name='מנהל מערכת',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
        else:
            print("משתמש admin כבר קיים")
        
        # יצירת סניף דוגמה
        branch = Branch.query.filter_by(name='כולל ראשי').first()
        if not branch:
            print("יוצר סניף דוגמה...")
            branch = Branch(
                name='כולל ראשי',
                address='רחוב הרב קוק 10, ירושלים',
                phone='02-1234567'
            )
            db.session.add(branch)
        else:
            print("סניף כבר קיים")
        
        # יצירת פרופיל תשלום דוגמה
        profile = PaymentProfile.query.filter_by(name='מסלול רגיל').first()
        if not profile:
            print("יוצר פרופיל תשלום דוגמה...")
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
            db.session.flush()  # כדי לקבל ID
            
            # הוספת בונוס תענית דיבור
            print("מוסיף בונוס תענית דיבור...")
            bonus = BonusRule(
                payment_profile_id=profile.id,
                name='תענית דיבור',
                bonus_type='daily',
                amount=10.0,
                description='בונוס יומי עבור שמירת תענית דיבור'
            )
            db.session.add(bonus)
        else:
            print("פרופיל תשלום כבר קיים")
        
        # שמירת השינויים
        db.session.commit()
        print("✅ בסיס הנתונים אותחל בהצלחה!")
        print("\n📋 פרטי התחברות:")
        print("   שם משתמש: admin")
        print("   סיסמה: admin123")
        print("\n🚀 כעת תוכל להפעיל את השרת עם: python run.py")

if __name__ == '__main__':
    init_database()