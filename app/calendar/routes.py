from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.calendar import bp
from app.models import SystemCalendar, CalendarEvent, db, DayTypeDefinition
from datetime import datetime, date
import calendar

@bp.route('/')
@login_required
def index():
    """לוח שנה ראשי"""
    year = request.args.get('year', type=int, default=date.today().year)
    month = request.args.get('month', type=int, default=date.today().month)
    
    # יצירת נתוני לוח שנה
    cal = calendar.Calendar(6)  # Sunday as first day (6)
    month_days = cal.monthdayscalendar(year, month)
    
    # שמות חודשים בעברית
    hebrew_months = [
        'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני',
        'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'
    ]
    
    # חישוב חודש קודם והבא
    if month == 1:
        prev_month = {'year': year - 1, 'month': 12}
    else:
        prev_month = {'year': year, 'month': month - 1}
    
    if month == 12:
        next_month = {'year': year + 1, 'month': 1}
    else:
        next_month = {'year': year, 'month': month + 1}
    
    # קבלת אירועים לחודש
    from sqlalchemy import extract
    events = CalendarEvent.query.filter(
        extract('year', CalendarEvent.date) == year,
        extract('month', CalendarEvent.date) == month,
        CalendarEvent.is_active == True
    ).all()
    
    # יצירת dictionary של אירועים לפי תאריך
    events_by_date = {}
    for event in events:
        event_date = event.date
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)
    
    # קבלת ימים מוגדרים בלוח שנה (עם סוג יום)
    system_calendar_days = SystemCalendar.query.filter(
        extract('year', SystemCalendar.date) == year,
        extract('month', SystemCalendar.date) == month
    ).all()
    
    # יצירת dictionary של ימי מערכת לפי תאריך
    system_days_by_date = {}
    for sys_day in system_calendar_days:
        system_days_by_date[sys_day.date] = sys_day
    
    # יצירת מבנה שבועות עבור התבנית
    calendar_weeks = []
    for week in month_days:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append({
                    'date': None,
                    'events': [],
                    'system_day': None
                })
            else:
                day_date = date(year, month, day)
                day_events = events_by_date.get(day_date, [])
                system_day = system_days_by_date.get(day_date)
                week_days.append({
                    'date': day_date,
                    'events': day_events,
                    'system_day': system_day
                })
        calendar_weeks.append(week_days)
    
    # אירועים קרובים (השבוע הקרוב)
    from datetime import timedelta
    today = date.today()
    week_from_now = today + timedelta(days=7)
    upcoming_events = CalendarEvent.query.filter(
        CalendarEvent.date >= today,
        CalendarEvent.date <= week_from_now,
        CalendarEvent.is_active == True
    ).order_by(CalendarEvent.date, CalendarEvent.time).all()
    
    # קבלת כל סוגי הימים הפעילים לסניף הנוכחי
    day_types = DayTypeDefinition.query.filter_by(
        branch_id=current_user.branch_id,
        is_active=True
    ).order_by(DayTypeDefinition.display_order, DayTypeDefinition.name).all()
    
    return render_template('calendar/index.html',
                         calendar_weeks=calendar_weeks,
                         current_year=year,
                         current_month=month,
                         month_name=hebrew_months[month-1],
                         prev_month=prev_month,
                         next_month=next_month,
                         today=date.today(),
                         upcoming_events=upcoming_events,
                         day_types=day_types)

@bp.route('/manage')
@login_required
def manage():
    """ניהול לוח שנה מערכתי"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    # קבלת כל האירועים
    events = CalendarEvent.query.filter(
        CalendarEvent.is_active == True
    ).order_by(CalendarEvent.date.desc(), CalendarEvent.time.desc()).all()
    
    return render_template('calendar/manage.html', events=events)

@bp.route('/add_event', methods=['POST'])
@login_required
def add_event():
    """הוספת אירוע חדש"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לביצוע פעולה זו', 'error')
        return redirect(url_for('calendar.index'))
    
    title = request.form.get('title')
    event_date_str = request.form.get('date')
    event_time_str = request.form.get('time')
    event_type = request.form.get('type', 'event')
    description = request.form.get('description')
    
    if title and event_date_str:
        try:
            # המרת התאריך
            event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            
            # המרת השעה אם קיימת
            event_time = None
            if event_time_str:
                event_time = datetime.strptime(event_time_str, '%H:%M').time()
            
            # יצירת אירוע חדש
            new_event = CalendarEvent(
                title=title,
                description=description,
                date=event_date,
                time=event_time,
                event_type=event_type,
                created_by=current_user.id
            )
            
            db.session.add(new_event)
            db.session.commit()
            
            flash('האירוע נוסף בהצלחה', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'שגיאה בהוספת האירוע: {str(e)}', 'error')
    else:
        flash('נא למלא את השדות הנדרשים', 'error')
    
    return redirect(url_for('calendar.index'))

@bp.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """מחיקת אירוע"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לביצוע פעולה זו', 'error')
        return redirect(url_for('calendar.index'))
    
    try:
        event = CalendarEvent.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        flash('האירוע נמחק בהצלחה', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'שגיאה במחיקת האירוע: {str(e)}', 'error')
    
    return redirect(url_for('calendar.manage'))

@bp.route('/set_day_type', methods=['POST'])
@login_required
def set_day_type():
    """הגדרת סוג יום לתאריך/ים"""
    if not current_user.is_admin():
        return {'success': False, 'message': 'אין לך הרשאה'}, 403
    
    try:
        data = request.get_json()
        dates = data.get('dates', [])
        day_type_id = data.get('day_type_id')
        
        if not dates:
            return {'success': False, 'message': 'לא נבחרו תאריכים'}, 400
        
        # אם day_type_id הוא None או 'null', נמחק את ההגדרה
        if day_type_id in [None, 'null', '']:
            for date_str in dates:
                day_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                sys_day = SystemCalendar.query.filter_by(date=day_date).first()
                if sys_day:
                    db.session.delete(sys_day)
            db.session.commit()
            return {'success': True, 'message': f'{len(dates)} ימים עודכנו לימים רגילים'}
        
        # המרת day_type_id למספר
        day_type_id = int(day_type_id)
        
        # בדיקה שסוג היום קיים
        day_type = DayTypeDefinition.query.get(day_type_id)
        if not day_type:
            return {'success': False, 'message': 'סוג יום לא נמצא'}, 404
        
        # עדכון כל התאריכים
        updated_count = 0
        for date_str in dates:
            day_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # בדיקה אם כבר קיים רשומה ליום זה
            sys_day = SystemCalendar.query.filter_by(date=day_date).first()
            if sys_day:
                # עדכון קיים
                sys_day.day_type_id = day_type_id
            else:
                # יצירת חדש
                sys_day = SystemCalendar(
                    date=day_date,
                    day_type_id=day_type_id
                )
                db.session.add(sys_day)
            updated_count += 1
        
        db.session.commit()
        return {'success': True, 'message': f'{updated_count} ימים עודכנו ל-{day_type.name}'}
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': f'שגיאה: {str(e)}'}, 500