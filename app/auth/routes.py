from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse
from app.auth import bp
from app.models import User
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = bool(request.form.get('remember_me'))
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('שם משתמש או סיסמה שגויים', 'error')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('המשתמש לא פעיל במערכת', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember_me)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))