from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.payment_profiles import bp
from app.models import PaymentProfile, BonusRule, db

@bp.route('/')
@login_required
def list():
    """רשימת פרופילי תשלום"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    profiles = PaymentProfile.query.filter_by(is_active=True).order_by(PaymentProfile.name).all()
    return render_template('payment_profiles/list.html', profiles=profiles)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """הוספת פרופיל תשלום חדש"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        from datetime import time
        
        # יצירת פרופיל חדש
        profile = PaymentProfile(
            name=request.form['name'],
            default_entry_time=time.fromisoformat(request.form['default_entry_time']),
            default_exit_time=time.fromisoformat(request.form['default_exit_time']),
            payment_method=request.form['payment_method'],
            daily_amount=float(request.form['daily_amount']) if request.form.get('daily_amount') else None,
            monthly_target=float(request.form['monthly_target']) if request.form.get('monthly_target') else None,
            enable_late_penalty=bool(request.form.get('enable_late_penalty')),
            late_penalty_method=request.form.get('late_penalty_method'),
            late_penalty_amount=float(request.form['late_penalty_amount']) if request.form.get('late_penalty_amount') else 0,
            late_penalty_interval=int(request.form['late_penalty_interval']) if request.form.get('late_penalty_interval') else 15,
            enable_absence_penalty=bool(request.form.get('enable_absence_penalty')),
            absence_penalty_method=request.form.get('absence_penalty_method', 'full_day')
        )
        
        try:
            db.session.add(profile)
            db.session.commit()
            flash(f'פרופיל התשלום "{profile.name}" נוסף בהצלחה', 'success')
            return redirect(url_for('payment_profiles.list'))
        except Exception as e:
            db.session.rollback()
            flash('שגיאה בהוספת הפרופיל', 'error')
    
    return render_template('payment_profiles/form.html', action='add')

@bp.route('/<int:id>')
@login_required
def view(id):
    """צפייה בפרופיל תשלום"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    profile = PaymentProfile.query.get_or_404(id)
    return render_template('payment_profiles/view.html', profile=profile)