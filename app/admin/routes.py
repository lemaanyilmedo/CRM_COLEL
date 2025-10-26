from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.admin import bp
from app.models import User, Branch, db

@bp.route('/users')
@login_required
def users():
    """ניהול משתמשים"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
    users = User.query.order_by(User.full_name).all()
    return render_template('admin/users.html', users=users)

@bp.route('/branches')
@login_required
def branches():
    """ניהול סניפים"""
    if not current_user.is_admin():
        flash('אין לך הרשאה לצפות בעמוד זה', 'error')
        return redirect(url_for('main.index'))
    
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