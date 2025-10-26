from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.avrech import bp
from app.models import Avrech, Branch, PaymentProfile, db

@bp.route('/')
@login_required
def list():
    """רשימת אברכים"""
    search = request.args.get('search', '')
    branch_id = request.args.get('branch_id', type=int)
    
    query = Avrech.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            (Avrech.first_name.contains(search)) |
            (Avrech.last_name.contains(search)) |
            (Avrech.id_number.contains(search))
        )
    
    if branch_id:
        query = query.filter_by(branch_id=branch_id)
    
    avrechim = query.order_by(Avrech.first_name, Avrech.last_name).all()
    branches = Branch.query.filter_by(is_active=True).all()
    
    return render_template('avrech/list.html', 
                         avrechim=avrechim, 
                         branches=branches,
                         search=search,
                         selected_branch=branch_id)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """הוספת אברך חדש"""
    if request.method == 'POST':
        avrech = Avrech(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            id_number=request.form['id_number'],
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            branch_id=request.form.get('branch_id', type=int) or None,
            payment_profile_id=request.form['payment_profile_id']
        )
        
        try:
            db.session.add(avrech)
            db.session.commit()
            flash(f'האברך {avrech.full_name} נוסף בהצלחה', 'success')
            return redirect(url_for('avrech.list'))
        except Exception as e:
            db.session.rollback()
            flash('שגיאה בהוספת האברך. בדוק שמספר הזהות אינו קיים במערכת', 'error')
    
    branches = Branch.query.filter_by(is_active=True).all()
    payment_profiles = PaymentProfile.query.filter_by(is_active=True).all()
    
    return render_template('avrech/form.html', 
                         branches=branches,
                         payment_profiles=payment_profiles,
                         action='add')

@bp.route('/<int:id>')
@login_required
def view(id):
    """צפייה באברך"""
    from datetime import date
    avrech = Avrech.query.get_or_404(id)
    
    # סטטיסטיקות חודש נוכחי
    today = date.today()
    monthly_summary = avrech.get_monthly_attendance_summary(today.year, today.month)
    monthly_total = sum([log.net_daily_amount or 0 for log in monthly_summary['logs']])
    
    return render_template('avrech/view.html', 
                         avrech=avrech,
                         monthly_stats=monthly_summary,
                         monthly_total=monthly_total)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """עריכת אברך"""
    avrech = Avrech.query.get_or_404(id)
    
    if request.method == 'POST':
        avrech.first_name = request.form['first_name']
        avrech.last_name = request.form['last_name']
        avrech.id_number = request.form['id_number']
        avrech.phone = request.form.get('phone')
        avrech.email = request.form.get('email')
        avrech.branch_id = request.form.get('branch_id', type=int) or None
        avrech.payment_profile_id = request.form['payment_profile_id']
        
        try:
            db.session.commit()
            flash(f'פרטי האברך {avrech.full_name} עודכנו בהצלחה', 'success')
            return redirect(url_for('avrech.view', id=id))
        except Exception as e:
            db.session.rollback()
            flash('שגיאה בעדכון הפרטים', 'error')
    
    branches = Branch.query.filter_by(is_active=True).all()
    payment_profiles = PaymentProfile.query.filter_by(is_active=True).all()
    
    return render_template('avrech/form.html', 
                         avrech=avrech,
                         branches=branches,
                         payment_profiles=payment_profiles,
                         action='edit')