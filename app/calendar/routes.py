from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.calendar import bp
from app.models import SystemCalendar, db

@bp.route('/')
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