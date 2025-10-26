from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.attendance import bp
from app.models import Avrech, AttendanceLog, SystemCalendar, db
from datetime import datetime, date, time

@bp.route('/')
@bp.route('/daily')
@login_required
def daily():
    """רישום נוכחות יומי"""
    selected_date = request.args.get('date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()
    
    # בדיקה האם זה יום עבודה
    if not SystemCalendar.is_working_day(selected_date):
        flash(f'היום {selected_date.strftime("%d/%m/%Y")} מוגדר כיום חופש', 'warning')
    
    # שליפת כל האברכים הפעילים
    avrechim = Avrech.query.filter_by(is_active=True).order_by(Avrech.first_name, Avrech.last_name).all()
    
    # שליפת נתוני נוכחות קיימים לתאריך זה
    attendance_data = {}
    existing_logs = AttendanceLog.query.filter_by(date=selected_date).all()
    for log in existing_logs:
        attendance_data[log.avrech_id] = log
    
    return render_template('attendance/daily.html', 
                         avrechim=avrechim,
                         attendance_data=attendance_data,
                         selected_date=selected_date)

@bp.route('/save_daily', methods=['POST'])
@login_required
def save_daily():
    """שמירת נתוני נוכחות יומי"""
    selected_date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    
    saved_count = 0
    errors = []
    
    for avrech_id in request.form.getlist('avrech_ids'):
        avrech_id = int(avrech_id)
        
        # שליפת הנתונים מהטופס
        entry_time_str = request.form.get(f'entry_time_{avrech_id}')
        exit_time_str = request.form.get(f'exit_time_{avrech_id}')
        status = request.form.get(f'status_{avrech_id}', 'present')
        taanit_dibur = bool(request.form.get(f'taanit_dibur_{avrech_id}'))
        
        try:
            # חיפוש או יצירת רשומת נוכחות
            log = AttendanceLog.query.filter_by(avrech_id=avrech_id, date=selected_date).first()
            if not log:
                log = AttendanceLog(avrech_id=avrech_id, date=selected_date)
                db.session.add(log)
            
            # עדכון הנתונים
            if entry_time_str:
                log.entry_time = datetime.strptime(entry_time_str, '%H:%M').time()
            else:
                log.entry_time = None
                
            if exit_time_str:
                log.exit_time = datetime.strptime(exit_time_str, '%H:%M').time()
            else:
                log.exit_time = None
            
            log.status = status
            log.taanit_dibur_bonus = taanit_dibur
            
            # חישוב איחורים ויציאות מוקדמות
            avrech = Avrech.query.get(avrech_id)
            if avrech and avrech.payment_profile:
                profile = avrech.payment_profile
                
                # חישוב איחור
                if log.entry_time and profile.default_entry_time:
                    entry_datetime = datetime.combine(selected_date, log.entry_time)
                    expected_datetime = datetime.combine(selected_date, profile.default_entry_time)
                    if entry_datetime > expected_datetime:
                        log.late_minutes = int((entry_datetime - expected_datetime).total_seconds() / 60)
                    else:
                        log.late_minutes = 0
                
                # חישוב יציאה מוקדמת
                if log.exit_time and profile.default_exit_time:
                    exit_datetime = datetime.combine(selected_date, log.exit_time)
                    expected_datetime = datetime.combine(selected_date, profile.default_exit_time)
                    if exit_datetime < expected_datetime:
                        log.early_exit_minutes = int((expected_datetime - exit_datetime).total_seconds() / 60)
                    else:
                        log.early_exit_minutes = 0
                
                # חישוב סכומים
                log.calculate_amounts()
            
            saved_count += 1
            
        except Exception as e:
            errors.append(f'שגיאה בשמירת נתוני {avrech.full_name}: {str(e)}')
    
    try:
        db.session.commit()
        flash(f'נתוני נוכחות נשמרו בהצלחה עבור {saved_count} אברכים', 'success')
        if errors:
            for error in errors:
                flash(error, 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'שגיאה בשמירת הנתונים: {str(e)}', 'error')
    
    return redirect(url_for('attendance.daily', date=selected_date.strftime('%Y-%m-%d')))

@bp.route('/history')
@login_required
def history():
    """היסטוריית נוכחות"""
    avrech_id = request.args.get('avrech_id', type=int)
    month = request.args.get('month', type=int, default=date.today().month)
    year = request.args.get('year', type=int, default=date.today().year)
    
    query = AttendanceLog.query
    
    if avrech_id:
        query = query.filter_by(avrech_id=avrech_id)
    
    # סינון לפי חודש ושנה
    query = query.filter(
        db.extract('month', AttendanceLog.date) == month,
        db.extract('year', AttendanceLog.date) == year
    )
    
    logs = query.order_by(AttendanceLog.date.desc()).all()
    avrechim = Avrech.query.filter_by(is_active=True).order_by(Avrech.first_name).all()
    
    return render_template('attendance/history.html',
                         logs=logs,
                         avrechim=avrechim,
                         selected_avrech=avrech_id,
                         selected_month=month,
                         selected_year=year)