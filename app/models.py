from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """משתמש מערכת"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'admin', 'employee'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

class Branch(db.Model):
    """סניף כולל"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    avrechim = db.relationship('Avrech', backref='branch', lazy=True)

class PaymentProfile(db.Model):
    """פרופיל תשלום - הגדרות חישוב המלגה"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # הגדרות שעות
    default_entry_time = db.Column(db.Time, nullable=False)  # שעת כניסה רגילה
    default_exit_time = db.Column(db.Time, nullable=False)   # שעת יציאה רגילה
    
    # הגדרות תשלום בסיס
    payment_method = db.Column(db.String(20), nullable=False)  # 'daily_fixed', 'monthly_target'
    daily_amount = db.Column(db.Float)      # סכום יומי קבוע
    monthly_target = db.Column(db.Float)    # יעד חודשי
    
    # הגדרות איחורים
    enable_late_penalty = db.Column(db.Boolean, default=False)
    late_penalty_method = db.Column(db.String(20))  # 'fixed_amount', 'per_minute'
    late_penalty_amount = db.Column(db.Float, default=0)
    late_penalty_interval = db.Column(db.Integer, default=15)  # דקות
    max_late_per_month = db.Column(db.Integer, default=10)
    
    # הגדרות יציאה מוקדמת
    enable_early_exit_penalty = db.Column(db.Boolean, default=False)
    early_exit_penalty_method = db.Column(db.String(20))
    early_exit_penalty_amount = db.Column(db.Float, default=0)
    early_exit_penalty_interval = db.Column(db.Integer, default=15)
    
    # הגדרות היעדרות
    enable_absence_penalty = db.Column(db.Boolean, default=True)
    absence_penalty_method = db.Column(db.String(20), default='full_day')  # 'full_day', 'fixed_amount'
    absence_penalty_amount = db.Column(db.Float, default=0)
    max_absences_per_month = db.Column(db.Integer, default=5)
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    avrechim = db.relationship('Avrech', backref='payment_profile', lazy=True)
    bonuses = db.relationship('BonusRule', backref='payment_profile', lazy=True, cascade='all, delete-orphan')

class BonusRule(db.Model):
    """חוק בונוס"""
    id = db.Column(db.Integer, primary_key=True)
    payment_profile_id = db.Column(db.Integer, db.ForeignKey('payment_profile.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False)
    bonus_type = db.Column(db.String(20), nullable=False)  # 'daily', 'sequence'
    amount = db.Column(db.Float, nullable=False)
    
    # עבור בונוס רצף
    sequence_days = db.Column(db.Integer)
    break_penalty_type = db.Column(db.String(20))  # 'full_reset', 'daily_loss', 'partial_penalty'
    break_penalty_amount = db.Column(db.Float, default=0)
    
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Avrech(db.Model):
    """אברך"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    # קישורים
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    payment_profile_id = db.Column(db.Integer, db.ForeignKey('payment_profile.id'), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date, default=datetime.utcnow().date())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance_logs = db.relationship('AttendanceLog', backref='avrech', lazy=True, order_by='AttendanceLog.date.desc()')
    bonus_records = db.relationship('BonusRecord', backref='avrech', lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_monthly_attendance_summary(self, year, month):
        """סיכום נוכחות חודשי"""
        from sqlalchemy import extract, and_
        
        logs = AttendanceLog.query.filter(
            and_(
                AttendanceLog.avrech_id == self.id,
                extract('year', AttendanceLog.date) == year,
                extract('month', AttendanceLog.date) == month
            )
        ).all()
        
        present_days = len([log for log in logs if log.status != 'absent'])
        absent_days = len([log for log in logs if log.status == 'absent'])
        total_late_minutes = sum([log.late_minutes or 0 for log in logs])
        total_early_exit_minutes = sum([log.early_exit_minutes or 0 for log in logs])
        
        return {
            'present_days': present_days,
            'absent_days': absent_days,
            'total_late_minutes': total_late_minutes,
            'total_early_exit_minutes': total_early_exit_minutes,
            'logs': logs
        }

class AttendanceLog(db.Model):
    """יומן נוכחות"""
    id = db.Column(db.Integer, primary_key=True)
    avrech_id = db.Column(db.Integer, db.ForeignKey('avrech.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    entry_time = db.Column(db.Time)
    exit_time = db.Column(db.Time)
    
    # חישובים אוטומטיים
    late_minutes = db.Column(db.Integer, default=0)
    early_exit_minutes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20))  # 'present', 'late', 'early_exit', 'absent'
    
    # בונוסים יומיים
    taanit_dibur_bonus = db.Column(db.Boolean, default=False)
    
    # חישוב תשלום
    daily_base_amount = db.Column(db.Float, default=0)
    penalties_amount = db.Column(db.Float, default=0)
    bonuses_amount = db.Column(db.Float, default=0)
    net_daily_amount = db.Column(db.Float, default=0)
    
    # הערות
    notes = db.Column(db.Text)
    manual_override = db.Column(db.Boolean, default=False)
    manual_amount = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('avrech_id', 'date', name='unique_avrech_date'),)
    
    def calculate_amounts(self):
        """חישוב סכומי התשלום היומי"""
        if not self.avrech or not self.avrech.payment_profile:
            return
        
        profile = self.avrech.payment_profile
        
        # חישוב סכום בסיס
        if profile.payment_method == 'daily_fixed':
            self.daily_base_amount = profile.daily_amount or 0
        elif profile.payment_method == 'monthly_target':
            # יחושב לפי ימי הלימוד החודש
            working_days = SystemCalendar.get_working_days_in_month(self.date.year, self.date.month)
            if working_days > 0:
                self.daily_base_amount = (profile.monthly_target or 0) / working_days
        
        # חישוב קנסות
        penalties = 0
        
        # קנס איחור
        if profile.enable_late_penalty and self.late_minutes > 0:
            if profile.late_penalty_method == 'fixed_amount':
                intervals = (self.late_minutes - 1) // profile.late_penalty_interval + 1
                penalties += intervals * profile.late_penalty_amount
            elif profile.late_penalty_method == 'per_minute':
                penalties += self.late_minutes * profile.late_penalty_amount
        
        # קנס יציאה מוקדמת
        if profile.enable_early_exit_penalty and self.early_exit_minutes > 0:
            if profile.early_exit_penalty_method == 'fixed_amount':
                intervals = (self.early_exit_minutes - 1) // profile.early_exit_penalty_interval + 1
                penalties += intervals * profile.early_exit_penalty_amount
            elif profile.early_exit_penalty_method == 'per_minute':
                penalties += self.early_exit_minutes * profile.early_exit_penalty_amount
        
        # קנס היעדרות
        if self.status == 'absent' and profile.enable_absence_penalty:
            if profile.absence_penalty_method == 'full_day':
                penalties = self.daily_base_amount
            elif profile.absence_penalty_method == 'fixed_amount':
                penalties += profile.absence_penalty_amount
        
        self.penalties_amount = penalties
        
        # חישוב בונוסים יומיים
        bonuses = 0
        for bonus_rule in profile.bonuses:
            if bonus_rule.bonus_type == 'daily':
                if bonus_rule.name == 'תענית דיבור' and self.taanit_dibur_bonus:
                    bonuses += bonus_rule.amount
        
        self.bonuses_amount = bonuses
        
        # סכום נטו
        if self.manual_override and self.manual_amount is not None:
            self.net_daily_amount = self.manual_amount
        else:
            self.net_daily_amount = max(0, self.daily_base_amount - penalties + bonuses)

class BonusRecord(db.Model):
    """רשומת בונוס (עבור בונוסי רצף)"""
    id = db.Column(db.Integer, primary_key=True)
    avrech_id = db.Column(db.Integer, db.ForeignKey('avrech.id'), nullable=False)
    bonus_rule_id = db.Column(db.Integer, db.ForeignKey('bonus_rule.id'), nullable=False)
    
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    current_sequence = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'broken'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bonus_rule = db.relationship('BonusRule', backref='records')

class SystemCalendar(db.Model):
    """לוח שנה מערכתי"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    day_type = db.Column(db.String(20), nullable=False, default='regular')  # 'regular', 'holiday', 'special'
    description = db.Column(db.String(200))
    
    # הגדרות מיוחדות ליום
    custom_entry_time = db.Column(db.Time)
    custom_exit_time = db.Column(db.Time)
    custom_daily_rate = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get_working_days_in_month(year, month):
        """מספר ימי עבודה בחודש"""
        from calendar import monthrange
        from sqlalchemy import extract, and_
        
        days_in_month = monthrange(year, month)[1]
        
        # ספירת ימי חופש
        holiday_count = SystemCalendar.query.filter(
            and_(
                extract('year', SystemCalendar.date) == year,
                extract('month', SystemCalendar.date) == month,
                SystemCalendar.day_type == 'holiday'
            )
        ).count()
        
        return days_in_month - holiday_count
    
    @staticmethod
    def is_working_day(date):
        """בדיקה האם יום עבודה"""
        calendar_day = SystemCalendar.query.filter_by(date=date).first()
        if calendar_day:
            return calendar_day.day_type != 'holiday'
        # ברירת מחדל - כל יום הוא יום עבודה חוץ משבת
        return date.weekday() != 5  # 5 = Saturday