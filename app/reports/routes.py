from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import login_required, current_user
from app.reports import bp
from app.models import Avrech, AttendanceLog, db
from datetime import date, datetime
import csv
import io

@bp.route('/')
@bp.route('/monthly')
@login_required
def monthly():
    """דוח תשלומים חודשי"""
    month = request.args.get('month', type=int, default=date.today().month)
    year = request.args.get('year', type=int, default=date.today().year)
    branch_id = request.args.get('branch_id', type=int)
    
    # בניית שאילתה
    query = Avrech.query.filter_by(is_active=True)
    if branch_id:
        query = query.filter_by(branch_id=branch_id)
    
    avrechim = query.order_by(Avrech.first_name, Avrech.last_name).all()
    
    # חישוב נתונים לכל אברך
    report_data = []
    for avrech in avrechim:
        monthly_summary = avrech.get_monthly_attendance_summary(year, month)
        total_amount = sum([log.net_daily_amount or 0 for log in monthly_summary['logs']])
        base_amount = sum([log.daily_base_amount or 0 for log in monthly_summary['logs']])
        penalties = sum([log.penalties_amount or 0 for log in monthly_summary['logs']])
        bonuses = sum([log.bonuses_amount or 0 for log in monthly_summary['logs']])
        
        report_data.append({
            'avrech': avrech,
            'present_days': monthly_summary['present_days'],
            'absent_days': monthly_summary['absent_days'],
            'late_minutes': monthly_summary['total_late_minutes'],
            'base_amount': base_amount,
            'penalties': penalties,
            'bonuses': bonuses,
            'total_amount': total_amount
        })
    
    return render_template('reports/monthly.html',
                         report_data=report_data,
                         selected_month=month,
                         selected_year=year,
                         selected_branch=branch_id)

@bp.route('/export_csv')
@login_required
def export_csv():
    """ייצוא דוח לCSV"""
    month = request.args.get('month', type=int, default=date.today().month)
    year = request.args.get('year', type=int, default=date.today().year)
    
    # יצירת הדוח
    output = io.StringIO()
    writer = csv.writer(output)
    
    # כותרות
    writer.writerow([
        'שם מלא', 'ת.ז.', 'סניף', 'ימי נוכחות', 'ימי היעדרות', 
        'דקות איחור', 'מלגת בסיס', 'קיזוזים', 'בונוסים', 'סכום נטו'
    ])
    
    avrechim = Avrech.query.filter_by(is_active=True).all()
    for avrech in avrechim:
        monthly_summary = avrech.get_monthly_attendance_summary(year, month)
        total_amount = sum([log.net_daily_amount or 0 for log in monthly_summary['logs']])
        base_amount = sum([log.daily_base_amount or 0 for log in monthly_summary['logs']])
        penalties = sum([log.penalties_amount or 0 for log in monthly_summary['logs']])
        bonuses = sum([log.bonuses_amount or 0 for log in monthly_summary['logs']])
        
        writer.writerow([
            avrech.full_name,
            avrech.id_number,
            avrech.branch.name if avrech.branch else '',
            monthly_summary['present_days'],
            monthly_summary['absent_days'],
            monthly_summary['total_late_minutes'],
            base_amount,
            penalties,
            bonuses,
            total_amount
        ])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename=salary_report_{year}_{month:02d}.csv'
    
    return response