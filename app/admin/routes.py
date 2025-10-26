from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, Branch, db, DayTypeDefinition

@bp.route('/users')
@login_required
def users():
    """ניהול משתמשים"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    users = User.query.order_by(User.full_name).all()
    return render_template('admin/users.html', users=users)

@bp.route('/branches', methods=['GET', 'POST'])
@login_required
def branches():
    """ניהול סניפים"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # הוספת סניף חדש
        name = request.form.get('name')
        description = request.form.get('description')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        if name:
            try:
                branch = Branch(
                    name=name,
                    address=address,
                    phone=phone
                )
                db.session.add(branch)
                db.session.commit()
                flash(f'הסניף "{name}" נוסף בהצלחה', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'שגיאה בהוספת הסניף: {str(e)}', 'error')
        else:
            flash('יש למלא את שם הסניף', 'error')
        
        return redirect(url_for('admin.branches'))
    
    branches = Branch.query.order_by(Branch.name).all()
    return render_template('admin/branches.html', branches=branches)

@bp.route('/system_settings')
@login_required
def system_settings():
    """הגדרות מערכת"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('admin/system_settings.html')

@bp.route('/day_types', methods=['GET', 'POST'])
@login_required
def day_types():
    """ניהול סוגי ימים"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    # Get selected branch or default to first
    selected_branch_id = request.args.get('branch_id', type=int)
    if not selected_branch_id:
        first_branch = Branch.query.first()
        if first_branch:
            selected_branch_id = first_branch.id
    
    if request.method == 'POST':
        # הוספת סוג יום חדש
        from datetime import time
        
        branch_id = int(request.form.get('branch_id'))
        name = request.form.get('name')
        description = request.form.get('description')
        payment_multiplier = float(request.form.get('payment_multiplier', 1.0))
        is_working_day = request.form.get('is_working_day') == 'on'
        is_default = request.form.get('is_default') == 'on'
        
        # שעות
        entry_hour = int(request.form.get('entry_hour', 8))
        entry_minute = int(request.form.get('entry_minute', 0))
        exit_hour = int(request.form.get('exit_hour', 13))
        exit_minute = int(request.form.get('exit_minute', 0))
        
        # קיזוזים
        enable_late_penalty = request.form.get('enable_late_penalty') == 'on'
        late_penalty_amount = float(request.form.get('late_penalty_amount', 0))
        late_grace_minutes = int(request.form.get('late_grace_minutes', 0))
        
        enable_early_exit_penalty = request.form.get('enable_early_exit_penalty') == 'on'
        early_exit_penalty_amount = float(request.form.get('early_exit_penalty_amount', 0))
        
        # בונוסים
        enable_daily_bonus = request.form.get('enable_daily_bonus') == 'on'
        daily_bonus_amount = float(request.form.get('daily_bonus_amount', 0))
        daily_bonus_description = request.form.get('daily_bonus_description', '')
        
        display_color = request.form.get('display_color', '#3498db')
        
        if name:
            try:
                day_type = DayTypeDefinition(
                    branch_id=branch_id,
                    name=name,
                    description=description,
                    payment_multiplier=payment_multiplier,
                    is_working_day=is_working_day,
                    is_default=is_default,
                    default_entry_time=time(entry_hour, entry_minute),
                    default_exit_time=time(exit_hour, exit_minute),
                    enable_late_penalty=enable_late_penalty,
                    late_penalty_amount=late_penalty_amount,
                    late_grace_minutes=late_grace_minutes,
                    enable_early_exit_penalty=enable_early_exit_penalty,
                    early_exit_penalty_amount=early_exit_penalty_amount,
                    enable_daily_bonus=enable_daily_bonus,
                    daily_bonus_amount=daily_bonus_amount,
                    daily_bonus_description=daily_bonus_description,
                    display_color=display_color
                )
                db.session.add(day_type)
                db.session.commit()
                flash(f'סוג היום "{name}" נוסף בהצלחה', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'שגיאה בהוספת סוג היום: {str(e)}', 'error')
        else:
            flash('יש למלא את שם סוג היום', 'error')
        
        return redirect(url_for('admin.day_types', branch_id=branch_id))
    
    # Get all branches for dropdown
    branches = Branch.query.filter_by(is_active=True).order_by(Branch.name).all()
    
    # Get day types for selected branch
    day_types = []
    if selected_branch_id:
        day_types = DayTypeDefinition.query.filter_by(
            branch_id=selected_branch_id,
            is_active=True
        ).order_by(DayTypeDefinition.display_order, DayTypeDefinition.name).all()
    
    return render_template('admin/day_types.html', 
                         day_types=day_types,
                         branches=branches,
                         selected_branch_id=selected_branch_id)

@bp.route('/day_types/delete/<int:id>', methods=['POST'])
@login_required
def delete_day_type(id):
    """מחיקת סוג יום"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לביצוע פעולה זו', 'error')
        return redirect(url_for('main.index'))
    
    try:
        day_type = DayTypeDefinition.query.get_or_404(id)
        day_type.is_active = False
        db.session.commit()
        flash(f'סוג היום "{day_type.name}" נמחק בהצלחה', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'שגיאה במחיקת סוג היום: {str(e)}', 'error')
    
    return redirect(url_for('admin.day_types'))