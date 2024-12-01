from flask import render_template, redirect, url_for
from flask_login import login_required
from app.admin import bp
from app.models import User, Service, ServiceRequest

@bp.route('/')
@login_required
def home():
    return render_template('admin/home.html')

@bp.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/services')
@login_required
def services():
    services = Service.query.all()
    return render_template('admin/services.html', services=services)