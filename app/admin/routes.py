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