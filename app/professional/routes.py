from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.professional import bp
from app.models import ServiceRequest

@bp.route('/')
@login_required
def home():
    return render_template('professional/home.html')

@bp.route('/requests')
@login_required
def requests():
    service_requests = ServiceRequest.query.filter_by(professional_id=current_user.id).all()
    return render_template('professional/requests.html', requests=service_requests)

@bp.route('/profile')
@login_required
def profile():
    return render_template('professional/profile.html')