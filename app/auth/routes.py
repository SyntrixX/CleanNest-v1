from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.models import User, Professional, Customer, Admin
from app import db

ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin123'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin.home'))
            elif user.role == 'professional':
                return redirect(url_for('professional.home'))
            else:
                return redirect(url_for('customer.home'))
        flash('Invalid email or password')
    return render_template('auth/login.html')

@bp.route('/register/customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        
        user = User(email=email, role='customer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        customer = Customer(user_id=user.id, name=name, phone=phone, address=address, city=city)
        db.session.add(customer)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_customer.html')

@bp.route('/register/professional', methods=['GET', 'POST'])
def register_professional():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        service_category = request.form.get('service_category')
        experience = request.form.get('experience')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        
        user = User(email=email, role='professional')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        professional = Professional(user_id=user.id, name=name, service_category=service_category, experience=experience, phone=phone, address=address, city=city)
        db.session.add(professional)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register_professional.html')

@bp.route('/register/admin', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(email=email, role='admin')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                admin = Admin(user_id=user.id)
                db.session.add(admin)
                db.session.commit()
                
                flash('Admin registration successful. Please log in.')
                return redirect(url_for('auth.login'))
            else:
                flash('Admin user already exists.')
        else:
            flash('Invalid admin credentials.')
    return render_template('auth/register_admin.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))