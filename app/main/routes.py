from flask import render_template, current_app
from flask_login import login_required, current_user
from app.main import bp
from app.models import Avrech, AttendanceLog, Branch
from datetime import datetime, date
from sqlalchemy import func, extract

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    """דשבורד ראשי"""
    today = date.today()
    
    # סטטיסטיקות כלליות
    total_avrechim = Avrech.query.filter_by(is_active=True).count()
    total_branches = Branch.query.filter_by(is_active=True).count()
    
    # נוכחות היום
    today_attendance = AttendanceLog.query.filter_by(date=today).all()
    present_today = len([log for log in today_attendance if log.status != 'absent'])
    absent_today = len([log for log in today_attendance if log.status == 'absent'])
    late_today = len([log for log in today_attendance if log.status == 'late'])
    
    # רשימה מפורטת של אברכים עם מצב נוכחות
    avrechim_list = []
    for avrech in Avrech.query.filter_by(is_active=True).all():
        # מצב נוכחות היום
        today_log = AttendanceLog.query.filter_by(
            avrech_id=avrech.id,
            date=today
        ).first()
        
        # חישוב סכום חודשי מצטבר
        monthly_summary = avrech.get_monthly_attendance_summary(today.year, today.month)
        monthly_total = sum([log.net_daily_amount or 0 for log in monthly_summary['logs']])
        
        avrech_data = {
            'avrech': avrech,
            'today_status': today_log.status if today_log else 'לא הוזן',
            'today_entry': today_log.entry_time if today_log else None,
            'today_exit': today_log.exit_time if today_log else None,
            'monthly_total': monthly_total,
            'branch_name': avrech.branch.name if avrech.branch else 'ללא סניף'
        }
        avrechim_list.append(avrech_data)
    
    return render_template('main/dashboard.html',
                         total_avrechim=total_avrechim,
                         total_branches=total_branches,
                         present_today=present_today,
                         absent_today=absent_today,
                         late_today=late_today,
                         avrechim_list=avrechim_list,
                         today=today)