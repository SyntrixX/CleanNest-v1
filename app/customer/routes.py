from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app import db
from app.customer import bp
from app.models import Service, ServiceRequest, Customer

@bp.route('/')
@login_required
def home():
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash('Customer profile not found.', 'danger')
        return redirect(url_for('customer.home'))  # Changed from 'main.home'
    pending_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='pending').all()
    active_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='active').all()
    completed_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status='completed').all()
    recent_requests = ServiceRequest.query.filter_by(customer_id=customer.id).order_by(ServiceRequest.created_at.desc()).limit(5).all()
    return render_template('customer/home.html', customer=customer, pending_requests=pending_requests, active_requests=active_requests, completed_requests=completed_requests, recent_requests=recent_requests)

@bp.route('/services')
@login_required
def services():
    services = Service.query.all()
    return render_template('customer/services.html', services=services)

@bp.route('/requests')
@login_required
def requests():
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash('Customer profile not found.', 'danger')
        return redirect(url_for('customer.home'))
    status = request.args.get('status', 'pending')
    service_requests = ServiceRequest.query.filter_by(customer_id=customer.id, status=status).all()
    return render_template('customer/requests.html', requests=service_requests, status=status)

@bp.route('/submit_request', methods=['POST'])
@login_required
def submit_request():
    service_id = request.form.get('service_id')
    preferred_date = request.form.get('preferred_date')
    preferred_time = request.form.get('preferred_time')
    notes = request.form.get('notes')
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash('Customer profile not found.', 'danger')
        return redirect(url_for('customer.home'))  # Changed from 'main.home'
    new_request = ServiceRequest(service_id=service_id, customer_id=customer.id, preferred_date=preferred_date, preferred_time=preferred_time, notes=notes, status='pending')
    db.session.add(new_request)
    db.session.commit()
    return redirect(url_for('customer.requests', status='pending'))

@bp.route('/submit_feedback/<int:request_id>', methods=['POST'])
@login_required
def submit_feedback(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.rating = request.form.get('rating')
    service_request.feedback = request.form.get('feedback')
    db.session.commit()
    return redirect(url_for('customer.requests', status='completed'))

@bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        # Update customer details with form data
        customer.name = request.form['name']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        # Handle profile image upload if provided
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image.filename != '':
                # Save the profile image and update the customer profile_image attribute
                filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                customer.profile_image = filename
        db.session.commit()
    return render_template('customer/update_profile.html', customer=customer)

@bp.route('/request_detail/<int:request_id>')
@login_required
def request_detail(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    return render_template('customer/request_detail.html', request=service_request)