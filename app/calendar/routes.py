from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.calendar import bp
from app.models import SystemCalendar, db
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
    
    # יצירת מבנה שבועות עבור התבנית
    calendar_weeks = []
    for week in month_days:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append({
                    'date': None,
                    'events': []
                })
            else:
                day_date = date(year, month, day)
                week_days.append({
                    'date': day_date,
                    'events': []  # כאן נוכל להוסיף אירועים מהמסד נתונים
                })
        calendar_weeks.append(week_days)
    
    return render_template('calendar/index.html',
                         calendar_weeks=calendar_weeks,
                         current_year=year,
                         current_month=month,
                         month_name=hebrew_months[month-1],
                         prev_month=prev_month,
                         next_month=next_month,
                         today=date.today(),
                         upcoming_events=[])

@bp.route('/manage')
@login_required
def manage():
    """ניהול לוח שנה מערכתי"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    year = request.args.get('year', type=int, default=2024)
    month = request.args.get('month', type=int, default=1)
    
    return render_template('calendar/manage.html', year=year, month=month)

@bp.route('/add_event', methods=['POST'])
@login_required
def add_event():
    """הוספת אירוע חדש"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לביצוע פעולה זו', 'error')
        return redirect(url_for('calendar.index'))
    
    title = request.form.get('title')
    event_date = request.form.get('date')
    event_time = request.form.get('time')
    event_type = request.form.get('type', 'event')
    description = request.form.get('description')
    
    if title and event_date:
        try:
            # כאן נוסיף את האירוע למסד הנתונים
            flash('האירוע נוסף בהצלחה', 'success')
        except Exception as e:
            flash('שגיאה בהוספת האירוע', 'error')
    else:
        flash('נא למלא את השדות הנדרשים', 'error')
    
    return redirect(url_for('calendar.index'))